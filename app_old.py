import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from pathlib import Path
import time

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

DOCUMENTS_DIR = "documents"
DELAY_BETWEEN_REQUESTS = 1  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 3  # seconds

def get_pdf_text(pdf_paths):
   text = ""
   for pdf_path in pdf_paths:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
   return text

def get_pdf_files_from_directory():
    """Load all PDF files from the documents directory"""
    pdf_files = []
    if os.path.exists(DOCUMENTS_DIR):
        pdf_files = list(Path(DOCUMENTS_DIR).glob("*.pdf"))
    return pdf_files
   
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=1000,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    """Create vectorstore with retry logic and rate limiting"""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        request_timeout=60,
    )
    
    retry_count = 0
    last_error = None
    
    while retry_count < MAX_RETRIES:
        try:
            st.info(f"Creating embeddings (attempt {retry_count + 1}/{MAX_RETRIES})...")
            vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
            vector_store.save_local("faiss_index")
            return vector_store
            
        except Exception as e:
            last_error = str(e)
            retry_count += 1
            
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = RETRY_DELAY * (2 ** (retry_count - 1))  # Exponential backoff
                st.warning(f"Rate limit hit. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            elif retry_count < MAX_RETRIES:
                st.warning(f"Error creating embeddings. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                break
    
    st.error(f"Failed to create embeddings after {MAX_RETRIES} attempts: {last_error}")
    raise Exception(f"Failed to create vectorstore: {last_error}")

def get_conversation_chain():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3
    )
    return model


def user_input(user_question):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            request_timeout=60,
        )
        
        # Add delay before loading vector store
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
        new_db = FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

        docs = new_db.similarity_search(user_question, k=4)
        chain = get_conversation_chain()
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = f"""Answer the question as detailed as possible from the provided context.
            If you don't know the answer, say you don't know.

            Ommit any confidential information from the context in your answer ex. Credential ID: 1234567890, etc. inform that you canot provide the answer due to the confidential information in the context.

            Context:{context}
            Question:{user_question}
            Answer:
            """

        response = chain.invoke(prompt)
        print(response.content)
        st.write("Reply:", response.content)
        
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            st.error("⏳ Rate limit exceeded. Please wait a few minutes before asking another question.")
        else:
            st.error(f"Error processing question: {str(e)}")

def main():
    st.set_page_config("Chat with Multiple PDFs")
    st.header("Chat with Multiple PDFs")
    
    st.info("💡 Rate limiting enabled: 1-second delays between API calls to avoid quota exhaustion. Automatic retries with exponential backoff if rate limits are hit.")

    # Get PDF files from documents directory and process them
    pdf_files = get_pdf_files_from_directory()
    
    if pdf_files:
        # Check if vector store already exists to avoid re-processing
        if not os.path.exists("faiss_index"):
            with st.spinner("Loading and processing PDFs (this may take a moment)..."):
                raw_text = get_pdf_text(pdf_files)
                text_chunks = get_text_chunks(raw_text)
                get_vectorstore(text_chunks)
            st.success("PDFs processed successfully!")
        
        user_question = st.text_input("Ask a question about the content of the PDFs:")
        if user_question:
            user_input(user_question)
    else:
        st.warning(f"No PDF files found in the '{DOCUMENTS_DIR}' folder. Please add PDF files there and refresh.")
        st.info(f"Create a '{DOCUMENTS_DIR}' folder in your project and add PDF files to it.")

if __name__ == "__main__":    
    main()