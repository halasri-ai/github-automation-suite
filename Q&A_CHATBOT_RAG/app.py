# ---------------------------
# Imports
# ---------------------------
import os
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime

import streamlit as st
import requests
import nltk
from fpdf import FPDF

from pypdf import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import google.generativeai as genai

nltk.download("punkt", quiet=True)

# ---------------------------
# Configuration
# ---------------------------
# Load environment variables from .env file
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    st.warning("⚠️ Please set your GENAI_API_KEY in the .env file.")
else:
    genai.configure(api_key=GENAI_API_KEY)

# ---------------------------
# Helpers
# ---------------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([p.extract_text() or "" for p in reader.pages])


def extract_text_from_repo(folder_path):
    text_data = ""
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel = os.path.relpath(file_path, folder_path)
            text_data += f"\n\n=== FILE: {rel} ===\n"
            try:
                if file.endswith(
                    (".txt", ".md", ".py", ".json", ".yaml", ".yml", ".csv")
                ):
                    with open(file_path, "r", errors="ignore") as f:
                        text_data += f.read()
                elif file.endswith(".pdf"):
                    with open(file_path, "rb") as f:
                        text_data += extract_text_from_pdf(f)
            except Exception as e:
                text_data += f"[Error reading {file}: {e}]"
    return text_data


@st.cache_data(show_spinner=False)
def download_and_extract_repo(repo_url):
    temp_dir = tempfile.mkdtemp()
    try:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        zip_url = f"{repo_url}/archive/refs/heads/main.zip"
        resp = requests.get(zip_url, timeout=60)
        if resp.status_code != 200:
            zip_url = f"{repo_url}/archive/refs/heads/master.zip"
            resp = requests.get(zip_url, timeout=60)
        zip_path = os.path.join(temp_dir, f"{repo_name}.zip")
        with open(zip_path, "wb") as f:
            f.write(resp.content)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(temp_dir)
        matches = list(Path(temp_dir).glob(f"{repo_name}*"))
        return str(matches[0]) if matches else temp_dir
    except Exception as e:
        raise RuntimeError(f"Repo extraction failed: {e}")


def chunk_text(text, chunk_size=800, overlap=100):
    # Clean and split text safely
    text = text.replace("\r", " ").replace("\n", " ").strip()
    if not text:
        return []
    splitter = CharacterTextSplitter(
        separator=" ",
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = splitter.split_text(text)
    st.write(f"🧩 Created {len(chunks)} chunks for FAISS index")
    return chunks


@st.cache_resource(show_spinner=False)
def build_faiss_index(chunks):
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_texts(chunks, embedding=emb)


def retrieve_chunks(db, query, top_k=10):
    docs = db.similarity_search(query, k=top_k)
    chunks = [doc.page_content for doc in docs if doc.page_content.strip()]
    st.write(f"🔍 Retrieved {len(chunks)} relevant chunks for query: {query}")
    return chunks


# ---------------------------
# Gemini-based Generation
# ---------------------------
def generate_short_answer(chunks, query):
    if not chunks:
        return "⚠️ No relevant context found in the repository for this question."
    context = "\n".join(chunks)
    prompt = f"""
Use the context below to answer briefly.

Context:
{context}

Question: {query}
Answer:
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content(prompt)
    return resp.text.strip() if hasattr(resp, "text") else "⚠️ No answer generated."


def generate_detailed_explanation(chunks, query):
    if not chunks:
        return "⚠️ No detailed context found in the repository for this topic."
    context = "\n".join(chunks)
    prompt = f"""
You are an expert technical writer.
Using only the provided context, write a structured, clear, and informative explanation for the topic below.

Topic: {query}

Context:
{context}

Detailed Explanation:
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content(prompt)
    return resp.text.strip() if hasattr(resp, "text") else "⚠️ No explanation generated."


# ---------------------------
# PDF Creation (FIXED)
# ---------------------------
def clean_text_for_pdf(text):
    """Remove or replace characters that might cause issues in PDF"""
    if not text:
        return ""
    
    # First, normalize the text
    import unicodedata
    text = unicodedata.normalize('NFKD', text)
    
    # Replace common problematic characters
    replacements = {
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '—': '-',
        '–': '-',
        '…': '...',
        '\u2022': '*',  # bullet point
        '\u2013': '-',  # en dash
        '\u2014': '-',  # em dash
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Encode to latin-1, replacing unsupported characters
    try:
        text = text.encode('latin-1', 'ignore').decode('latin-1')
    except:
        # Fallback: keep only ASCII characters
        text = ''.join(char if ord(char) < 128 else '?' for char in text)
    
    # Remove control characters except newlines and tabs
    text = ''.join(char for char in text if char in '\n\t' or ord(char) >= 32)
    
    return text


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "RAG Knowledge Report", ln=True, align="C")
        self.ln(5)

    def chapter_title(self, num, label):
        self.set_font("Arial", "B", 14)
        # Clean the label text
        label = clean_text_for_pdf(label)
        self.cell(0, 10, f"{num}. {label}", ln=True)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font("Arial", "", 11)
        # Clean the body text
        text = clean_text_for_pdf(text)
        self.multi_cell(0, 7, text)
        self.ln(6)


def create_pdf(repo_url, qna_data):
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Add header
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "RAG Knowledge Report", ln=True, align="C")
        pdf.ln(5)
        
        # Add repository info
        pdf.set_font("Arial", size=12)
        repo_text = clean_text_for_pdf(str(repo_url))
        pdf.multi_cell(0, 8, f"Repository: {repo_text}")
        
        date_text = f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        pdf.multi_cell(0, 8, date_text)
        pdf.ln(10)

        for i, (question, short_ans, detailed) in enumerate(qna_data, start=1):
            # Clean all text before adding
            clean_question = clean_text_for_pdf(str(question))
            clean_short = clean_text_for_pdf(str(short_ans))
            clean_detailed = clean_text_for_pdf(str(detailed))
            
            # Add question as title
            pdf.set_font("Arial", "B", 14)
            pdf.multi_cell(0, 10, f"{i}. {clean_question}")
            pdf.ln(4)
            
            # Add short answer
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 7, "Short Answer:", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 7, clean_short)
            pdf.ln(6)
            
            # Add detailed explanation
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 7, "Detailed Explanation:", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 7, clean_detailed)
            pdf.ln(6)
            
            # Only add page if not the last item
            if i < len(qna_data):
                pdf.add_page()

        # Generate PDF - use dest parameter correctly
        output = pdf.output(dest='S')
        
        # Handle encoding based on type
        if isinstance(output, bytes):
            return output
        elif isinstance(output, str):
            return output.encode('latin-1', 'replace')
        else:
            st.error(f"Unexpected output type: {type(output)}")
            return b''
            
    except Exception as e:
        st.error(f"PDF generation error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        
        # Return minimal fallback PDF
        try:
            pdf_fallback = FPDF()
            pdf_fallback.add_page()
            pdf_fallback.set_font("Arial", size=12)
            pdf_fallback.cell(0, 10, "Error generating PDF", ln=True)
            pdf_fallback.cell(0, 10, "Please check the console for details", ln=True)
            
            fallback_output = pdf_fallback.output(dest='S')
            if isinstance(fallback_output, bytes):
                return fallback_output
            return fallback_output.encode('latin-1', 'replace')
        except:
            return b''


# ---------------------------
# Streamlit App
# ---------------------------
st.set_page_config(page_title="RAG Chat — Detailed PDF", layout="wide")
st.title("🤖 RAG Chat — GitHub Repository Assistant (Detailed PDF Export)")

# Session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "faiss_db" not in st.session_state:
    st.session_state["faiss_db"] = None
if "repo_path" not in st.session_state:
    st.session_state["repo_path"] = None

# ---------------------------
# Sidebar - Repository Loader
# ---------------------------
with st.sidebar:
    st.header("Repository")
    repo_url = st.text_input("GitHub Repo URL")

    if st.button("Load Repository"):
        with st.spinner("Loading and indexing repository..."):
            path = download_and_extract_repo(repo_url)
            text = extract_text_from_repo(path)
            st.write(f"🧾 Extracted text length: {len(text)} characters")
            chunks = chunk_text(text)
            st.session_state["faiss_db"] = build_faiss_index(chunks)
            st.session_state["repo_path"] = path
            st.success("✅ Repository loaded and indexed successfully!")

# ---------------------------
# Chat Interface
# ---------------------------
st.header("Chat")

# Display previous messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# Input for new question
user_input = st.chat_input("Ask your question (e.g., What is RAG?, What is chunking?)")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    db = st.session_state.get("faiss_db")

    if db:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chunks = retrieve_chunks(db, user_input, top_k=5)
                ans = generate_short_answer(chunks, user_input)
                st.session_state["messages"].append({"role": "assistant", "content": ans})
                st.write(ans)
    else:
        st.warning("⚠️ Please load a repository first.")

# ---------------------------
# Generate PDF
# ---------------------------
st.markdown("---")
st.subheader("📘 Generate Full Detailed PDF")

if st.button("Generate Detailed Knowledge PDF"):
    db = st.session_state.get("faiss_db")
    if not db:
        st.error("No repository loaded.")
    elif not repo_url:
        st.error("No repository URL found. Please load a repository first.")
    else:
        qna_data = []
        with st.spinner("Building detailed report based on your chat..."):
            user_questions = [
                msg["content"] for msg in st.session_state["messages"] if msg["role"] == "user"
            ]
            if not user_questions:
                st.warning("Ask at least one question before generating a report.")
            else:
                for q in user_questions:
                    chunks = retrieve_chunks(db, q, top_k=10)
                    short_ans = generate_short_answer(chunks, q)
                    detailed = generate_detailed_explanation(chunks, q)
                    qna_data.append((q, short_ans, detailed))
                
                st.info(f"Generating PDF with {len(qna_data)} Q&A pairs...")
                
                try:
                    pdf_bytes = create_pdf(repo_url, qna_data)
                    
                    if pdf_bytes and len(pdf_bytes) > 0:
                        st.success(f"📄 PDF generated successfully! Size: {len(pdf_bytes)} bytes")
                        filename = f"rag_detailed_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
                        st.download_button(
                            "📥 Download Detailed Knowledge Report",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                        )
                    else:
                        st.error("PDF generation resulted in empty file.")
                except Exception as e:
                    st.error(f"Failed to generate PDF: {str(e)}")
                    st.exception(e)