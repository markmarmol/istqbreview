"""
ISTQ Query Interface
Interactive UI to search ISTQ documents and get AI-powered answers
"""

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ISTQ Query Assistant",
    page_icon="📚",
    layout="wide"
)

# Title
st.markdown("# 📚 ISTQ Query Assistant")
st.markdown("Search ISTQ documents and get AI-powered answers to your testing questions")

# Check API keys
openai_key = os.environ.get('OPENAI_API_KEY')

if not openai_key:
    st.error("❌ OPENAI_API_KEY not found in .env file")
    st.info("Please add your OpenAI API key to the .env file to continue")
    st.stop()

# Initialize session state for caching
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "llm" not in st.session_state:
    st.session_state.llm = None
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False

# Load documents and initialize models
@st.cache_resource
def load_and_prepare_documents():
    """Load PDF documents and prepare vectorstore"""
    with st.spinner("Loading ISTQ documents..."):
        try:
            # Load PDFs
            loader = PyPDFDirectoryLoader("documents")
            documents = loader.load()
            
            # Chunk documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=50
            )
            chunks = text_splitter.split_documents(documents)
            
            # Create embeddings and vectorstore
            embeddings = OpenAIEmbeddings(api_key=openai_key)
            vectorstore = FAISS.from_documents(chunks, embeddings)
            
            return vectorstore, len(chunks)
        except Exception as e:
            st.error(f"Error loading documents: {e}")
            st.info("Make sure the 'documents' folder contains PDF files")
            return None, 0

@st.cache_resource
def initialize_llm():
    """Initialize ChatOpenAI LLM"""
    return ChatOpenAI(
        api_key=openai_key,
        model="gpt-3.5-turbo",
        temperature=0.3
    )

# Load resources
try:
    vectorstore, chunk_count = load_and_prepare_documents()
    llm = initialize_llm()
    
    if vectorstore:
        st.success(f"✅ System ready! Loaded {chunk_count} document chunks")
    else:
        st.stop()
        
except Exception as e:
    st.error(f"Error initializing system: {e}")
    st.stop()

# Query section
st.markdown("---")
st.markdown("## 🔍 Enter Your Question")

# Create two columns: one for input, one for button
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "Ask your ISTQ question:",
        placeholder="e.g., What is the difference between testing and debugging?",
        key="user_query"
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

# Process query
if search_button and query:
    with st.spinner("Searching documents and generating answer..."):
        try:
            # Search for relevant documents
            results = vectorstore.similarity_search(query, k=3)
            
            if results:
                # Prepare context
                context = "\n\n".join([doc.page_content for doc in results])
                
                # Create prompt
                prompt = f"""Based on the following ISTQ documentation, answer the question clearly and concisely.

ISTQ Documentation:
{context}

Question: {query}

Answer:"""
                
                # Get answer from LLM
                response = llm.invoke(prompt)
                answer = response.content if hasattr(response, 'content') else str(response)
                
                # Display answer
                st.markdown("---")
                st.markdown("## 💡 Answer")
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196f3;">
                {answer}
                </div>
                """, unsafe_allow_html=True)
                
                # Display source documents
                st.markdown("## 📖 Related Documentation")
                
                for idx, doc in enumerate(results, 1):
                    with st.expander(f"📄 Source {idx} - Page {doc.metadata.get('page', 'N/A')}", expanded=(idx==1)):
                        st.markdown(f"**File:** {doc.metadata.get('source', 'Unknown').split('/')[-1]}")
                        st.markdown(f"**Page:** {doc.metadata.get('page', 'N/A')}")
                        st.markdown("---")
                        st.markdown(f"""
                        <div style="background-color: #fff3e0; padding: 10px; border-radius: 8px;">
                        {doc.page_content}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No relevant documents found. Try rephrasing your question.")
                
        except Exception as e:
            st.error(f"Error processing query: {e}")

elif search_button and not query:
    st.warning("⚠️ Please enter a question first")

# Example queries section
st.markdown("---")
