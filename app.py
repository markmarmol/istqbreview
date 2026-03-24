import streamlit as st
import os
from pathlib import Path
import time
import random
import re
from questions import QUIZ_QUESTIONS
from dotenv import load_dotenv
import google.genai as genai
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

DOCUMENTS_DIR = "documents"
DELAY_BETWEEN_REQUESTS = 0.5
MAX_RETRIES = 3
RETRY_DELAY = 2

# Initialize vectorstore for document search
@st.cache_resource
def load_vectorstore():
    """Load and prepare ISTQ documents vectorstore"""
    try:
        openai_key = os.environ.get('OPENAI_API_KEY')
        if not openai_key:
            return None
        
        # Load PDFs
        loader = PyPDFDirectoryLoader("documents")
        documents = loader.load()
        
        # Chunk documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create vectorstore
        embeddings = OpenAIEmbeddings(api_key=openai_key)
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        return vectorstore
    except Exception as e:
        print(f"Error loading vectorstore: {e}")
        return None

def find_related_documents(question, vectorstore, k=4):
    """Find related documents for a given question"""
    if not vectorstore:
        return []
    
    try:
        results = vectorstore.similarity_search(question, k=k)
        return results
    except Exception as e:
        print(f"Error searching documents: {e}")
        return []


def strip_image_markdown(text):
    """Remove image markdown syntax from text"""
    # Remove all ![alt](path) patterns
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    return re.sub(image_pattern, '', text).strip()


def render_explanation_with_images(explanation_text):
    """Render explanation text with embedded images"""
    # Find all image references: ![alt](path)
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    # Split text by images
    parts = re.split(image_pattern, explanation_text)
    
    for i, part in enumerate(parts):
        if i % 3 == 0:  # Text part
            if part.strip():
                st.markdown(f"<p style='font-size: 18px; line-height: 1.8; word-wrap: break-word;'>{part}</p>", unsafe_allow_html=True)
        elif i % 3 == 2:  # Image path part (alt text is i-1)
            if os.path.exists(part):
                st.image(part, use_container_width=True)


def get_explanation_html(explanation_text):
    """Convert explanation text with images to HTML content"""
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    parts = re.split(image_pattern, explanation_text)
    
    html_content = ""
    for i, part in enumerate(parts):
        if i % 3 == 0:  # Text part
            if part.strip():
                html_content += f"<p style='font-size: 18px; line-height: 1.8; word-wrap: break-word;'>{part}</p>"
        elif i % 3 == 2:  # Image path part (alt text is i-1)
            if os.path.exists(part):
                html_content += f"<img src='{part}' style='max-width: 100%; border-radius: 8px; margin: 15px 0;'/>"
    
    return html_content


def render_explanation_box(title, explanation_text, bg_color, text_color, emoji):
    """Render explanation inside a colored box"""
    explanation_html = get_explanation_html(explanation_text)
    box_html = f"""<div style="padding: 30px; background-color: {bg_color}; border-radius: 15px;">
<h3 style="color: {text_color}; margin-top: 0; margin-bottom: 20px;">{emoji} {title}</h3>
{explanation_html}
</div>"""
    st.markdown(box_html, unsafe_allow_html=True)


def render_answer_options(options):
    """Render answer options"""
    options_html = f"""
<p><strong>A:</strong> {options[0]}</p>
<p><strong>B:</strong> {options[1]}</p>
<p><strong>C:</strong> {options[2]}</p>
<p><strong>D:</strong> {options[3]}</p>
"""
    st.markdown(options_html, unsafe_allow_html=True)

def get_pdf_files_from_directory():
    """Load all PDF files from the documents directory"""
    pdf_files = []
    if os.path.exists(DOCUMENTS_DIR):
        pdf_files = list(Path(DOCUMENTS_DIR).glob("*.pdf"))
    return pdf_files


def generate_explanation_with_retry(question, correct_answer, user_answer, options, is_correct):
    """Generate detailed explanation using AI with retry logic"""
    retry_count = 0
    last_error = None
    
    while retry_count < MAX_RETRIES:
        try:
            st.info(f"Generating explanation (attempt {retry_count + 1}/{MAX_RETRIES})...")
            
            if is_correct:
                prompt = f"""Provide a detailed and educational explanation for why this answer is correct:

Question: {question}

Correct Answer: {correct_answer} - {options[ord(correct_answer) - ord('A')]}

Explain:
1. Why this answer is correct
2. Key concepts involved
3. Common misconceptions to avoid

Keep the explanation concise but informative (2-3 sentences max)."""
            else:
                prompt = f"""Provide a detailed educational explanation for the correct answer:

Question: {question}

User's Answer: {user_answer} - {options[ord(user_answer) - ord('A')]}
Correct Answer: {correct_answer} - {options[ord(correct_answer) - ord('A')]}

Explain:
1. Why the correct answer is {correct_answer}
2. Why the user's answer is incorrect (if applicable)
3. Key concepts to understand
4. Add any real life examples or analogies to help clarify the concept

Keep the explanation concise but informative (2-3 sentences max)."""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "temperature": 0.3,  # Lower temp = faster
                }
            )
            time.sleep(DELAY_BETWEEN_REQUESTS)
            return response.text
            
        except Exception as e:
            last_error = str(e)
            retry_count += 1
            error_msg = str(e)
            
            st.error(f"Error generating explanation: {error_msg}")
            
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                wait_time = RETRY_DELAY * (2 ** (retry_count - 1))
                st.warning(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            elif retry_count < MAX_RETRIES:
                st.warning(f"Retrying explanation generation in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                break
    
    # Return default explanation if AI fails
    if last_error:
        return f"Unable to generate explanation. Error: {last_error}"
    return "Unable to generate AI explanation at this time. Please try again later."


def initialize_quiz():
    """Initialize quiz state in session"""
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.questions = []
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = {}
        st.session_state.quiz_completed = False


def display_quiz():
    """Display the quiz interface"""
    if not st.session_state.questions:
        st.error("No questions available. Please reload the quiz.")
        return
    
    # Randomize questions
    if "questions_randomized" not in st.session_state:
        random.shuffle(st.session_state.questions)
        st.session_state.questions_randomized = True
    
    current_q = st.session_state.current_question
    question_data = st.session_state.questions[current_q]
    
    # Display progress
    st.progress((current_q + 1) / len(st.session_state.questions))
    st.write(f"Question {current_q + 1} of {len(st.session_state.questions)}")
    
    # Display question
    st.subheader(question_data["question"])
    
    # Display options
    options = question_data["options"]
    correct_answer = question_data["correct_answer"]
    explanation = question_data["explanation"]
    
    # Render answer options in styled box
    render_answer_options(options)
    
    # Radio button for selection
    selected = st.radio(
        "Your answer:",
        options=["A", "B", "C", "D"],
        key=f"question_{current_q}",
        horizontal=True
    )
    
    # Button section - 2 columns only
    btn_col1, btn_col2 = st.columns(2, gap="small")
    
    with btn_col1:
        if st.button("Submit Answer", use_container_width=True):
            # Check if answer is correct
            is_correct = selected == correct_answer
            st.session_state.answers[current_q] = {
                "selected": selected,
                "correct": is_correct
            }
            
            if is_correct:
                st.session_state.score += 1
                st.success("✓ Correct!")
            else:
                st.error(f"✗ Incorrect. The correct answer is {correct_answer}")
            
            # Generate AI explanation
            with st.spinner("Generating detailed explanation..."):
                ai_explanation = generate_explanation_with_retry(
                    question_data["question"],
                    correct_answer,
                    selected,
                    options,
                    is_correct
                )
            
            # Store AI explanation in session state
            st.session_state.last_ai_explanation = ai_explanation
            st.session_state.answer_submitted = True
            st.rerun()
    
    with btn_col2:
        if st.button("End Quiz", use_container_width=True):
            st.session_state.quiz_completed = True
            st.rerun()
    
    # Display explanations side by side when answer is submitted
    if st.session_state.get("answer_submitted", False):
        st.markdown("---")
        st.subheader("📖 Explanations & ISTQ Sources")
        
        # Load vectorstore and find related documents
        vectorstore = load_vectorstore()
        related_docs = find_related_documents(question_data["question"], vectorstore, k=2)
        
        if related_docs:
            # 3-column layout: Default | AI | Related Documents
            exp_col1, exp_col2, exp_col3 = st.columns(3, gap="small")
        else:
            # 2-column layout if no related documents
            exp_col1, exp_col2 = st.columns(2, gap="small")
        
        with exp_col1:
            render_explanation_box(
                "Default Explanation",
                explanation,
                "#e8f4f8",
                "#0066cc",
                "📚"
            )
        
        with exp_col2:
            ai_explanation = st.session_state.get("last_ai_explanation", "")
            if ai_explanation and ai_explanation.strip():
                render_explanation_box(
                    "AI-Generated Explanation",
                    ai_explanation,
                    "#e8f5e9",
                    "#2e7d32",
                    "✨"
                )
            elif not ai_explanation:
                st.info("🔄 AI explanation generation is loading...")
        
        # Display related ISTQ documents if found
        if related_docs:
            with exp_col3:
                st.markdown("<div style='background-color: #fff3e0; padding: 20px; border-radius: 8px; border-left: 4px solid #ff9800;'><h3 style='margin-top: 0; margin-bottom: 20px; color: #ff9800;'>📖 ISTQ Syllabus Sources</h3>", unsafe_allow_html=True)
                
                for idx, doc in enumerate(related_docs, 1):
                    st.markdown(f"<div style='margin-bottom: 10px;'>", unsafe_allow_html=True)
                    with st.expander(f"Source {idx} - Page {doc.metadata.get('page', 'N/A')}", expanded=(idx==1)):
                        st.markdown(f"**File:** {doc.metadata.get('source', 'Unknown').split('/')[-1]}")
                        st.markdown(f"**Page:** {doc.metadata.get('page', 'N/A')}")
                        st.markdown("---")
                        st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Show message when no related documents found (only if we have 3 columns)
            if 'exp_col3' in locals():
                with exp_col3:
                    st.markdown("<div style='background-color: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #999;'>", unsafe_allow_html=True)
                    st.markdown("### 📖 ISTQ Syllabus Sources")
                    st.info("📌 No specific ISTQ syllabus sections found for this question. Review the default and AI explanations above.")
                    st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Next question button (shown after answer is submitted)
    if st.session_state.get("answer_submitted", False):
        if current_q < len(st.session_state.questions) - 1:
            if st.button("Next Question"):
                st.session_state.current_question += 1
                st.session_state.answer_submitted = False
                st.rerun()
        else:
            st.session_state.quiz_completed = True
            st.rerun()


def display_results():
    """Display quiz results"""
    st.header("Quiz Completed!")
    
    total_questions = len(st.session_state.questions)
    
    # Safeguard against division by zero
    if total_questions == 0:
        st.warning("No quiz data available. Returning to menu...")
        time.sleep(1)
        st.session_state.quiz_completed = False
        st.rerun()
        return
    
    score = st.session_state.score
    percentage = (score / total_questions) * 100
    
    # Display score
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Your Score", f"{score}/{total_questions}")
    
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    
    with col3:
        if percentage >= 80:
            st.metric("Grade", "A")
        elif percentage >= 70:
            st.metric("Grade", "B")
        elif percentage >= 60:
            st.metric("Grade", "C")
        else:
            st.metric("Grade", "F")
    
    # Display detailed results
    st.subheader("Detailed Results")
    
    for idx, question_data in enumerate(st.session_state.questions):
        with st.expander(f"Question {idx + 1}: {question_data['question'][:50]}..."):
            st.write("**Question:**", question_data["question"])
            
            if idx in st.session_state.answers:
                user_answer = st.session_state.answers[idx]["selected"]
                is_correct = st.session_state.answers[idx]["correct"]
                correct_answer = question_data["correct_answer"]
                
                if is_correct:
                    st.success(f"✓ Your answer: {user_answer} - Correct")
                else:
                    st.error(f"✗ Your answer: {user_answer} - Incorrect")
                    st.info(f"Correct answer: {correct_answer}")
            else:
                st.warning("Not answered")
            
            st.write("**Explanation:**", question_data["explanation"])
    
    # Restart quiz button
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Retake Quiz"):
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answers = {}
            st.session_state.quiz_completed = False
            st.session_state.questions_randomized = False
            st.rerun()
    
    with col2:
        if st.button("Back to Menu"):
            st.session_state.quiz_started = False
            st.session_state.quiz_completed = False
            st.session_state.questions = []
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answers = {}
            st.rerun()


def main():
    st.set_page_config(page_title="Quiz Generator", layout="wide", initial_sidebar_state="collapsed")
    st.header("📚 ISTQB MOCK EXAM")
    
    initialize_quiz()
    
    # Get PDF files
    pdf_files = get_pdf_files_from_directory()
    
    if not pdf_files:
        st.warning(f"No PDF files found in the '{DOCUMENTS_DIR}' folder.")
        st.info(f"Create a '{DOCUMENTS_DIR}' folder in your project and add PDF files to start.")
        return
    
    # Show files found
    st.info(f"Found {len(pdf_files)} PDF file(s)")
    
    if st.session_state.quiz_completed:
        # Show results
        display_results()
    
    elif st.session_state.quiz_started:
        # Show quiz
        display_quiz()
    
    else:
        # Show menu
        st.subheader("Quiz Menu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Available Documents:")
            for pdf_file in pdf_files:
                st.write(f"- {pdf_file.name}")
        
        with col2:
            st.write("### Quiz Information:")
            st.write(f"- **Number of Questions:** {len(QUIZ_QUESTIONS)}")
            st.write(f"- **Question Type:** Multiple Choice")
        
        if st.button("Start Quiz", key="start_button", use_container_width=True):
            try:
                st.session_state.questions = QUIZ_QUESTIONS.copy()
                st.session_state.quiz_started = True
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = {}
                st.session_state.answer_submitted = False
                
                st.success("Quiz loaded successfully! Starting quiz...")
                time.sleep(1)
                st.rerun()
            
            except Exception as e:
                st.error(f"Error loading quiz: {str(e)}")


if __name__ == "__main__":
    main()
