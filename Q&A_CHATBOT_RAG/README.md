🤖 RAG-Based GitHub Repository Q&A Chatbot
With Gemini-Powered Answers & Detailed PDF Export

This project is an end-to-end Retrieval-Augmented Q&A System built to analyze any public GitHub repository, retrieve the most relevant context using semantic search (FAISS), optionally generate answers using Google Gemini, and export a beautiful structured PDF knowledge report based on your questions.

It’s designed for:

Developers exploring unfamiliar repositories

Students studying large codebases

Documentation teams generating summaries

Anyone needing quick insights from GitHub repos

⭐ Key Features
🔍 1. GitHub Repository Loader

Provide any public GitHub URL

Automatically downloads & extracts the repo

Reads all .py, .md, .txt, .json, .yaml, .csv, and .pdf files

Skips binary files

🧩 2. Smart Chunking + FAISS Retrieval

Uses CharacterTextSplitter for clean chunking

Embeds chunks using sentence-transformers/all-MiniLM-L6-v2

Stores & retrieves chunks via FAISS vector search

Retrieves top-k chunks most relevant to your question

🧠 3. Google Gemini for Answer Generation

Gemini (via gemini-2.5-flash) generates:

Short answers

Detailed multi-section explanations

Ensured to stay grounded using the retrieved context.

📄 4. Detailed PDF Export

Auto-generates a robust knowledge report that includes:

All questions you asked in the chat

Short AI-generated answers

Deep explanations

Clean, readable formatting using FPDF

Automatic Unicode normalization

Error handling for non-Latin characters

💬 5. Interactive Chat Interface

Ask questions in natural language

Get immediate answers & retrieved chunks

Chat history preserved in session

Answers stored for PDF compilation

🏗️ Project Structure
QnA_Chatbot_RAG/
│
├── app.py                # Main Streamlit application
├── requirements.txt      # All Python dependencies
├── .env                  # API keys (not pushed to GitHub)
│
├── fonts/                # Optional - for PDF font customization
│   ├── DejaVuSans.ttf
│   ├── DejaVuSans.pkl
│   └── DejaVuSans.cw127.pkl
│
└── README.md

🔧 Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/<your-username>/QnA_Chatbot_RAG.git
cd QnA_Chatbot_RAG

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Add your Google Gemini API key

Create a .env file in the root directory:

GENAI_API_KEY=your_google_generative_ai_key_here

4️⃣ Run the application
streamlit run app.py

🚀 Usage Workflow
Step 1 — Load Repository

Paste any public GitHub repo URL into the sidebar.
The app will:

Download

Extract

Load text

Chunk

Embed

Build FAISS index

Step 2 — Ask Questions

Example:

“What is RAG?”

“Explain how chunking works in this repo”

“Describe the architecture of this project”

The app retrieves relevant text and Gemini produces:

Short direct answers

Detailed explanations

Step 3 — Generate PDF Report

Click "Generate Detailed Knowledge PDF"
The report includes:

Each question you asked

The short Gemini answer

A fully expanded explanation

Timestamp + repo reference

Great for:

Documentation

Study notes

Internal onboarding

Codebase analysis

🛠️ Technology Stack
📦 Core Libraries

Streamlit — UI & interaction

FAISS — semantic vector search

Sentence Transformers — MiniLM embeddings

LangChain Text Splitters — intelligent chunking

FPDF — PDF report generation

PyPDF — PDF text extraction

Requests — GitHub zip downloader

🤖 AI Model

gemini-2.5-flash (via Google Generative AI API)

✔️ Why Gemini?

Fast

Cost-efficient

Excellent for summarization

Grounded in provided context

📘 Example PDF Output Structure
RAG Knowledge Report  
Repository: https://github.com/example/repo  
Generated on: YYYY-MM-DD  

1. What is RAG?
Short Answer:
   <Gemini concise answer>

Detailed Explanation:
   <Multi-section explanation grounded in repo content>

2. Explain chunking in this repo.
Short Answer:
   ...

Detailed Explanation:
   ...

(Next Question...)

🧪 Limitations & Notes

Only public GitHub repositories are supported

Very large repos may take longer to index

PDF export uses safe Latin-1 fallback for special characters

.env must not be pushed to GitHub

🤝 Contributing

Pull requests are welcome!
Areas that can be improved:

Retrieval accuracy

UI design

Support for private GitHub repos

Optional offline model mode

📜 License

MIT License (recommended) — or specify your license here.

🙌 Acknowledgements

Google Gemini

LangChain

SentenceTransformers

Streamlit

FAISS