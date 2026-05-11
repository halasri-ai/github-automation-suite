🚀 Intelligent GitHub Automation Suite
Voice-Controlled Repository Creation → AI-Powered Code Analysis → RAG-Based Q&A ChatbotAn end-to-end automated pipeline from voice command to intelligent documentation.
📌 Table of Contents
Project Overview
System Architecture
Full Pipeline Workflow
System 1 — GitHub Voice Assistant
System 2 — Complete Repository Analyzer (PDF + PPT)
System 3 — RAG-Based Q&A Chatbot with PDF Export
Repository Link Transmission via CURL
Tech Stack
Project Structure
Installation & Setup
Usage Guide
Voice Commands Reference
Configuration
Deployment Considerations
Troubleshooting
Security
Contributing
License
Author & Acknowledgements
🧠 Project Overview
The Intelligent GitHub Automation Suite is a multi-system, AI-driven pipeline that automates the full lifecycle of GitHub repository management and analysis. It combines three independently designed systems into a single seamless workflow:
System 1 — GitHub Voice Assistant: A voice-controlled CLI tool that creates GitHub repositories, manages issues, PRs, branches, and collaborators — all through natural language spoken commands.
System 2 — Repository Analyzer: Automatically downloads any GitHub repo, performs deep file-level and architecture-level analysis using a cloud LLM, and generates a professional PDF report and PowerPoint presentation.
System 3 — RAG Chatbot: Builds a FAISS-backed vector database from the repository content, enabling an interactive Q&A chat interface powered by Google Gemini, with the ability to export the entire conversation as a structured PDF.
Once a repository is created and pushed in System 1, a single CURL command distributes the repository link to both System 2 and System 3, which then process it independently and concurrently on remote cloud machines.
🏗️ System Architecture
┌──────────────────────────────────────────────────────────────┐
│              USER (Local Machine)                            │
│                                                              │
│   🎙️ Voice Command → GitHub Voice Assistant (System 1)      │
│        ↓                                                     │
│   Repository Created & Local Folder Pushed                   │
│        ↓                                                     │
│   GitHub Repository URL Generated                            │
│        ↓                                                     │
│   curl -X POST "http://<endpoint>/receive" \                 │
│         -d '{"link": "<repo_url>"}'                          │
└────────────────────────┬─────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
┌─────────────────────┐   ┌─────────────────────────────────┐
│   ☁️  CLOUD VM A    │   │         ☁️  CLOUD VM B           │
│                     │   │                                  │
│  System 2:          │   │  System 3:                       │
│  Repo Analyzer      │   │  RAG Q&A Chatbot                 │
│                     │   │                                  │
│  • Download Repo    │   │  • Download Repo                 │
│  • Parse Files      │   │  • Extract Text                  │
│  • Chunk + LLM      │   │  • Chunk + Embed                 │
│  • Generate PDF     │   │  • FAISS Vector DB               │
│  • Generate PPT     │   │  • Gemini Q&A                    │
│                     │   │  • Export Chat PDF               │
└─────────────────────┘   └─────────────────────────────────┘
🔄 Full Pipeline Workflow
Step 1 — Voice-Controlled Repository Creation (Local Machine)
User launches the Voice Assistant (python main.py)
User speaks a command (e.g., "Create repository my-new-project")
Speech recognition converts voice to text
Flan-T5 AI model interprets the intent
GitHub API is called to create the repository
Local project folder is staged, committed, and pushed to GitHub via authenticated HTTPS
The system outputs the final GitHub repository URL
Step 2 — Distributing the Repository Link via CURL
User copies the repository URL
User sends it to a configured remote endpoint using a CURL POST request
The endpoint receives the JSON payload {"link": "<repo_url>"}
The endpoint forwards the link simultaneously to both Cloud VM A (System 2) and Cloud VM B (System 3)
Step 3 — System 2 Processing (Repository Analyzer)
Downloads the repository as a ZIP file (tries main then master branch)
Extracts all contents into a processing directory
Scans and filters relevant file types (ignores node_modules, .git, venv, etc.)
Splits file contents into optimally sized text chunks
Each chunk is sent to a cloud LLM for file-level analysis
Aggregated file summaries are synthesized into a global project-level report
Report is divided into 10 structured sections (see below)
A professional PDF and a PowerPoint presentation are generated and saved
Step 4 — System 3 Processing (RAG Chatbot)
Downloads and extracts the same repository independently
Reads all compatible file types (.py, .md, .txt, .json, .yaml, .csv, .pdf)
Splits combined text into smaller semantic chunks
Generates embeddings using sentence-transformers/all-MiniLM-L6-v2
Builds a FAISS vector store from all embeddings
Streamlit UI is ready for user interaction
User asks questions; top-ranked vector chunks are retrieved per question
Google Gemini generates a short answer and a detailed explanation for each query
All Q&A pairs are stored in session state
On clicking "Generate PDF", the entire chat history is compiled into a clean PDF report
🎙️ System 1 — GitHub Voice Assistant
Overview
A voice-controlled CLI tool for managing GitHub repositories, issues, pull requests, branches, collaborators, and GitHub Actions workflows — entirely through natural language speech or text input. Powered locally by the Flan-T5 AI model for intent detection.
Core Capabilities
Category	Features
Repository Management	Create, delete, push local folder, pull latest changes, auto-generate .gitignore
Collaboration	Add/remove collaborators, set permissions (read, write, admin)
Issue Tracking	Create issues, list open/closed issues, comment on issues, close issues
Pull Requests	Create PRs between branches, list PRs, merge PRs, comment on PRs
Branch Management	Create branches from any base, list all branches, delete branches
GitHub Actions	Create workflow templates (Python tests, deployment), check workflow status
Input Modes	Voice mode (microphone) or Text mode (keyboard), with auto-fallback
Technical Flow
Voice Input
    ↓
Speech Recognition (Google Speech API)
    ↓
Flan-T5 AI — Intent Detection & Natural Language Understanding
    ↓
Command Parser — Maps intent to GitHub action
    ↓
GitHub API / Git Commands (Executed locally)
    ↓
Text-to-Speech Response (pyttsx3)
Architecture Diagram
┌─────────────────────────────────────────────┐
│          User Input (Voice / Text)          │
└──────────────────┬──────────────────────────┘
                   ↓
        ┌──────────────────────┐
        │  Speech Recognition  │
        │   (Google API)       │
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │   Flan-T5 AI Model   │
        │  Natural Language    │
        │   Understanding      │
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │  Command Parser      │
        │  Intent Detection    │
        └──────────┬───────────┘
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
    ┌─────────┐       ┌─────────┐
    │ GitHub  │       │   Git   │
    │   API   │       │ Commands│
    └─────────┘       └─────────┘
          └────────┬────────┘
                   ↓
        ┌──────────────────────┐
        │    Text-to-Speech    │
        │  (pyttsx3 Engine)    │
        └──────────────────────┘
📊 System 2 — Complete Repository Analyzer (PDF + PPT)
Overview
An automated code analysis engine that downloads any GitHub repository, performs deep multi-level analysis using a cloud LLM (AWS Bedrock — Claude 3 Sonnet), and produces professional-grade PDF and PowerPoint documentation.
Functional Capabilities
Downloads the repository as a ZIP (with fallback: main → master)
Extracts and walks through all directory contents
Filters only valid source code and documentation file types
Skips irrelevant directories (node_modules, .git, __pycache__, venv, dist, build, etc.)
Uses RecursiveCharacterTextSplitter to split large files into 3000-token chunks (200 overlap)
Sends each chunk to the LLM for a concise 2–3 sentence file-level analysis
Aggregates per-file analyses into a condensed 1000–1500 word project summary
Generates 10 detailed report sections from the condensed summary
Report Sections Generated
#	Section	Description
1	Project Summary	Purpose, goals, and overall architecture
2	Tech Stack	All technologies, frameworks, libraries, and tools
3	File/Folder Structure	Directory organization and key components
4	Core Modules	Main modules and their individual functions
5	Data Flow & Logic	How data flows and how components interact
6	Code Quality Analysis	Readability, modularity, and best practices
7	Red Flags & Issues	Code smells, technical debt, scalability concerns
8	Security Risks	Vulnerabilities and security considerations
9	Performance Risks	Bottlenecks, resource management, inefficiencies
10	Refactor Suggestions	Actionable improvements and optimization tips
Technical Flow
Step 1 → Repo ZIP Download (main / master fallback)
Step 2 → File Filtering (valid extensions only, IGNORE_DIRS skipped)
Step 3 → Text Chunking (RecursiveCharacterTextSplitter, 3000 tokens)
Step 4 → Per-Chunk LLM Analysis (AWS Bedrock — Claude 3 Sonnet)
Step 5 → Per-File Summary Aggregation
Step 6 → Condensed Project Summary (1000–1500 words)
Step 7 → 10 Structured Section Generation via LLM
Step 8 → PDF Generation (ReportLab — professional layout)
Step 9 → PPT Generation (python-pptx — slide-based with icons)
Step 10 → Output: analysis_output/report_<timestamp>.pdf
          Output: analysis_output/presentation_<timestamp>.pptx
          Output: analysis_output/analysis_<timestamp>.txt
Supported File Types
.py .js .ts .tsx .jsx .java .cpp .c .h .hpp .html .css .scss .sass .less .json .md .txt .yaml .yml .xml .sql .sh .bash .go .rs .rb .php .swift .kt .scala .r .vue .svelte
Ignored Directories
node_modules .git __pycache__ dist build .venv env venv .idea __MACOSX logs tmp temp .next coverage .pytest_cache htmlcov site-packages
PDF Features
Title page with project name and generation timestamp
Section-wise structured layout with emoji headers
Tech Stack rendered as a formatted table
Red Flags and Security Risks highlighted in color-coded warning boxes
Bullet-point and paragraph formatting per section
Professional footer
PPT Features
Gradient title slide with project branding
Per-section content slides with color-coded accent bars
Emoji-based icon shapes per section type
Table slide for Tech Stack
Warning-styled slides for Red Flags and Security Risks
Auto-pagination: slides split automatically when content exceeds limits
Closing "Thank You" slide
💬 System 3 — RAG-Based Q&A Chatbot with PDF Export
Overview
An interactive Retrieval-Augmented Generation (RAG) chatbot built on top of FAISS vector search and Google Gemini. Allows any user to ask questions about a GitHub repository in natural language and get grounded, context-aware answers. At any point, the entire chat session can be exported as a structured PDF knowledge report.
Core Capabilities
Retrieval Pipeline
Downloads and extracts the repository ZIP
Reads all compatible file types: .py, .md, .txt, .json, .yaml, .csv, and embedded .pdf files
Combines all text and splits into optimally sized semantic chunks using CharacterTextSplitter
Generates sentence embeddings using sentence-transformers/all-MiniLM-L6-v2
Stores embeddings in a FAISS vector index for fast similarity search
Chat Interface (Streamlit)
User inputs the GitHub repository URL in the sidebar
System loads, extracts, embeds, and indexes the repository (one-time setup)
User asks questions in natural language
Top-K most relevant chunks are retrieved from FAISS per query
Google Gemini (gemini-2.5-flash) generates:
A short, direct answer
A detailed multi-section explanation grounded in the retrieved context
Full chat history is preserved across the session
PDF Export
User clicks "Generate Detailed Knowledge PDF" after interacting with the chatbot
System iterates through all stored Q&A pairs from the session
Generates a clean, multi-section PDF including:
Repository reference and generation timestamp
Each question asked by the user
The short Gemini-generated answer
The full detailed explanation
Output is downloadable directly from the Streamlit UI
Technical Flow
Step 1 → User inputs repo URL in Streamlit sidebar
Step 2 → Repo ZIP downloaded and extracted
Step 3 → File text extracted (all compatible formats)
Step 4 → Text split into chunks (CharacterTextSplitter)
Step 5 → Embeddings generated (all-MiniLM-L6-v2)
Step 6 → FAISS vector index built
Step 7 → User types question in chat
Step 8 → Top-K relevant chunks retrieved from FAISS
Step 9 → Chunks + question sent to Gemini (gemini-2.5-flash)
Step 10 → Short answer + detailed explanation displayed in UI
Step 11 → Q&A pair stored in session state
Step 12 → User clicks "Generate PDF"
Step 13 → All session Q&A compiled into structured PDF (FPDF)
Step 14 → PDF downloaded by user
📡 Repository Link Transmission via CURL
After System 1 generates the GitHub repository URL, the user sends it to a configured remote endpoint using a single CURL command. The endpoint forwards the link to both System 2 and System 3 running on separate cloud VMs.
CURL Command
curl -X POST "http://<your-endpoint>/receive" \
  -H "Content-Type: application/json" \
  -d '{"link": "https://github.com/<owner>/<repo>"}'
What the Endpoint Does
Receives the JSON payload containing the "link" field
Forwards the link to Cloud VM A → triggers System 2 (Repo Analyzer)
Forwards the link to Cloud VM B → triggers System 3 (RAG Chatbot)
Both systems operate independently and concurrently
🛠️ Tech Stack
System 1 — GitHub Voice Assistant
Component	Technology
Language	Python 3.9+
AI Model	Google Flan-T5 (local inference)
Speech Recognition	SpeechRecognition (Google Speech API)
Text-to-Speech	pyttsx3
GitHub Integration	PyGithub
NLP Tokenizer	Hugging Face Transformers
Environment Config	python-dotenv
System 2 — Repository Analyzer
Component	Technology
Language	Python 3.9+
LLM Backend	AWS Bedrock (Claude 3 Sonnet)
LLM Integration	LangChain (langchain-aws, langchain-text-splitters)
Text Chunking	RecursiveCharacterTextSplitter
PDF Generation	ReportLab
PPT Generation	python-pptx
File Handling	zipfile, os, subprocess
System 3 — RAG Chatbot
Component	Technology
Language	Python 3.9+
UI Framework	Streamlit
AI Model	Google Gemini (gemini-2.5-flash)
Embedding Model	sentence-transformers/all-MiniLM-L6-v2
Vector Database	FAISS
Text Chunking	LangChain CharacterTextSplitter
PDF Export	FPDF
PDF Reading	PyPDF
GitHub Download	Requests
API Config	Google Generative AI SDK
📁 Project Structure
intelligent-github-suite/
│
├── 📂 system1_voice_assistant/
│   ├── main.py                          # Main Voice Assistant application
│   ├── .env                             # GitHub token & username (NOT committed)
│   ├── .env.example                     # Template for environment variables
│   ├── requirements.txt                 # Dependencies for System 1
│   ├── .gitignore
│   │
│   ├── 📂 push/                         # Staging folder — local files to push
│   ├── 📂 local_repo/                   # Cloned repositories land here
│   └── 📂 .github/
│       └── workflows/
│           └── python-test.yml          # Auto-generated GitHub Actions workflow
│
├── 📂 system2_repo_analyzer/
│   ├── integrated_github_analyzer.py    # Main analyzer script
│   ├── requirements.txt                 # Dependencies for System 2
│   │
│   └── 📂 analysis_output/              # All generated files saved here
│       ├── analysis_<timestamp>.txt     # Raw text report
│       ├── report_<timestamp>.pdf       # Generated PDF
│       └── presentation_<timestamp>.pptx # Generated PowerPoint
│
├── 📂 system3_rag_chatbot/
│   ├── app.py                           # Main Streamlit application
│   ├── requirements.txt                 # Dependencies for System 3
│   ├── .env                             # Gemini API key (NOT committed)
│   │
│   └── 📂 fonts/                        # Optional — custom PDF fonts
│       ├── DejaVuSans.ttf
│       ├── DejaVuSans.pkl
│       └── DejaVuSans.cw127.pkl
│
├── 📂 endpoint/
│   └── receiver.py                      # CURL endpoint — distributes repo link
│
├── README.md                            # This file
└── architecture_workflow.pdf            # System architecture document
⚙️ Installation & Setup
Prerequisites
Python 3.9 or higher
A GitHub account with a Personal Access Token
AWS account with Bedrock access (for System 2)
Google Generative AI API key (for System 3)
A microphone (optional, for System 1 voice mode)
Two cloud VMs (for hosting System 2 and System 3 remotely)
System 1 — GitHub Voice Assistant
Step 1: Clone the repository
git clone https://github.com/YOUR_USERNAME/intelligent-github-suite.git
cd intelligent-github-suite/system1_voice_assistant
Step 2: Create and activate a virtual environment
# Windows
python -m venv venv
venv\Scripts\activate
# Linux / Mac
python3 -m venv venv
source venv/bin/activate
Step 3: Install dependencies
pip install -r requirements.txt
Note: First run downloads the Flan-T5-small model (~300MB). Ensure a stable internet connection.
Step 4: Install PyAudio (for voice mode)
Windows:
pip install pipwin
pipwin install pyaudio
Mac:
brew install portaudio
pip install pyaudio
Linux:
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
Step 5: Configure environment variables
cp .env.example .env
Edit .env:
GITHUB_TOKEN=ghp_your_personal_access_token_here
GITHUB_USERNAME=YourGitHubUsername
How to generate a GitHub Personal Access Token:
Go to: https://github.com/settings/tokens
Click "Generate new token (classic)"
Select scopes: repo, workflow, admin:org
Copy and paste into .env
System 2 — Repository Analyzer
Step 1: Navigate to the system folder
cd system2_repo_analyzer
Step 2: Install dependencies
pip install -r requirements.txt
Step 3: Configure AWS credentials
Edit integrated_github_analyzer.py and update the AWS_CONFIG block:
AWS_CONFIG = {
    'access_key': 'YOUR_AWS_ACCESS_KEY',
    'secret_key': 'YOUR_AWS_SECRET_KEY',
    'region': 'us-east-1',
    'model_id': 'anthropic.claude-3-sonnet-20240229-v1:0'
}
Security Note: Use environment variables or AWS IAM roles in production. Never hardcode credentials in source code.
System 3 — RAG Chatbot
Step 1: Navigate to the system folder
cd system3_rag_chatbot
Step 2: Install dependencies
pip install -r requirements.txt
Step 3: Configure the API key
Create a .env file:
GENAI_API_KEY=your_google_generative_ai_api_key_here
🚀 Usage Guide
Running System 1 — Voice Assistant
cd system1_voice_assistant
python main.py
On launch, choose your input mode:
🎤 Choose input mode — Voice (v) or Text (t) [auto fallback]: v
Type v for voice mode (requires a working microphone)
Type t for text/keyboard mode
If the microphone fails, the system automatically falls back to text mode
Running System 2 — Repository Analyzer
cd system2_repo_analyzer
python integrated_github_analyzer.py
Follow the prompts:
Enter '1' for GitHub URL or '2' for local folder: 1
📎 Enter GitHub repository URL: https://github.com/owner/repo
📊 Max files to analyze (default=40): 40
📄 Generate PDF and PPT? (Y/n): Y
Output files are saved in: analysis_output/
Running System 3 — RAG Chatbot
cd system3_rag_chatbot
streamlit run app.py
The Streamlit UI will open in your browser. Then:
Paste the GitHub repository URL in the sidebar
Click Load Repository — the system will download, extract, embed, and index the repo
Type your questions in the chat input
View short answers and detailed explanations in the UI
Click Generate Detailed Knowledge PDF to export the full chat session as a PDF
🗣️ Voice Commands Reference
Repository Operations
"Create repository <name>"
"Create repo <name>"
"Delete repository <name>"
"Push to <repo-name>"
"Push folder to <repo-name>"
"Pull from <repo-name>"
"Pull repository updates"
Issue Management
"Create issue titled '<title>' in repository <repo-name>"
"List issues in repository <repo-name>"
"Comment '<text>' on issue <number> in repository <repo-name>"
"Close issue <number> in repository <repo-name>"
Pull Requests
"Create pull request titled '<title>' from <branch> to <base> in repository <repo-name>"
"List pull requests in repository <repo-name>"
"Merge pull request <number> in repository <repo-name>"
"Comment '<text>' on pull request <number> in repository <repo-name>"
Branch Operations
"Create branch <branch-name> from <base-branch> in repository <repo-name>"
"List branches in repository <repo-name>"
"Delete branch <branch-name> in repository <repo-name>"
Collaborator Management
"Add collaborator <username> to repository <repo-name>"
# The assistant will ask: "What level of access should I give — read, write, or admin?"
GitHub Actions
"Create action in repository <repo-name>"
"Check workflow in repository <repo-name>"
🔧 Configuration
System 1 — Customize Voice Settings
In main.py:
# Words per minute (speech speed)
engine.setProperty('rate', 150)
# Volume (0.0 to 1.0)
engine.setProperty('volume', 1.0)
System 1 — Customize Speech Recognition Timeouts
def listen_command(timeout=6, phrase_time_limit=8):
    # Increase timeout if your commands are longer
System 1 — Change AI Model Size
# Use larger model for better natural language understanding
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
System 2 — Adjust Maximum Files Analyzed
When running the script, enter your preferred limit at the prompt:
📊 Max files to analyze (default=40): 60
System 2 — Add or Remove File Extensions
In integrated_github_analyzer.py:
VALID_EXTENSIONS = (
    '.py', '.js', '.ts', ...  # Add or remove extensions here
)
System 2 — Customize Ignored Directories
IGNORE_DIRS = {
    'node_modules', '.git', '__pycache__', ...  # Add custom dirs to skip
}
☁️ Deployment Considerations
Cloud VM Requirements
System	Compute	Notes
System 2 (Analyzer)	Higher compute	LLM inference, PDF/PPT generation — recommend 4+ vCPUs, 8GB+ RAM
System 3 (RAG Chatbot)	Moderate compute	Embedding + FAISS + Streamlit — recommend 2+ vCPUs, 4GB+ RAM
Secret Management
Store all tokens and API keys in environment variables or a secrets manager (e.g., AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault)
Never embed credentials directly in source code
.env files must be listed in .gitignore and never committed
Networking
The CURL endpoint (receiver.py) must be publicly accessible or reachable from the local machine
Both Cloud VMs must have outbound internet access to:
github.com — for repository downloads
AWS Bedrock endpoints (System 2)
Google Generative AI API (System 3)
Process Management
Use systemd, supervisor, or pm2 to keep the CURL endpoint and Streamlit app running persistently on cloud VMs
Consider using tmux or screen for manual deployments
🐛 Troubleshooting
Problem	Cause	Solution
Microphone unavailable	PyAudio not installed correctly	Reinstall PyAudio for your OS (see Installation section)
GitHub token invalid	Wrong token or expired scopes	Regenerate token with repo, workflow, admin:org scopes
Could not understand audio	Background noise or unclear speech	Speak clearly near mic, reduce background noise, or switch to text mode (t)
Model download fails	No internet or HuggingFace cache issue	Check connection, run rm -rf ~/.cache/huggingface and retry
Repo not downloading	Branch name mismatch	System automatically tries main then master — verify branch exists
PDF encoding issues	Non-Latin characters in content	System applies Unicode normalization and Latin-1 safe fallback automatically
LLM connection errors	Invalid API key or no internet on VM	Verify API key in environment variables and confirm outbound internet access
Embedding failures	FAISS version mismatch	Install FAISS compatible with your Python version (faiss-cpu for most cases)
Empty PDF or PPT	No sections parsed from report	Check that the report text contains === SECTION NAME === delimiters
Streamlit not loading	Port conflict	Run streamlit run app.py --server.port 8502
🛡️ Security
Best Practices
✅ Use Personal Access Tokens — never commit GitHub passwords
✅ Rotate tokens regularly
✅ Use fine-grained tokens with only the required scopes
✅ Store all credentials in .env files and never push them to version control
✅ Use cloud secret managers in production environments
✅ The staging directory used for pushing files is automatically cleaned up after each push operation
Files That Must Never Be Committed
The .gitignore automatically excludes:
.env
venv/
push/
local_repo/
current_repo.txt
__pycache__/
analysis_output/
*.pdf
*.pptx
📊 Performance Reference
Operation	Approximate Time	Notes
Voice recognition	1–2 seconds	Depends on speech clarity and network
Flan-T5 intent inference	0.5–1 second	Local CPU inference
GitHub API calls	0.5–2 seconds	Depends on network latency
Repo push (folder)	3–10 seconds	Depends on folder size
Repo ZIP download	5–30 seconds	Depends on repo size and network
Per-chunk LLM analysis (System 2)	2–5 seconds	Depends on AWS Bedrock response time
Full repo analysis (40 files)	10–25 minutes	Includes all LLM calls and section generation
FAISS index build (System 3)	30–120 seconds	Depends on repo size
Gemini answer generation	3–8 seconds	Short + detailed answer per query
PDF export (chatbot)	5–15 seconds	Depends on number of Q&A pairs
🤝 Contributing
Contributions are welcome. To contribute:
Fork the repository
Create a feature branch: git checkout -b feature/your-feature-name
Make your changes and commit: git commit -m "Add your feature"
Push to your fork: git push origin feature/your-feature-name
Open a Pull Request with a clear description of what you changed and why
Areas for Improvement
Retrieval accuracy in System 3 (hybrid search, re-ranking)
Support for private GitHub repositories (token-based download)
Web-based UI for System 2 output visualization
Support for additional LLM providers (OpenAI, Cohere, Mistral)
Slack or Discord integration for report delivery
Mobile app for voice commands (iOS / Android)
Team analytics dashboard built from multiple repo analyses
Optional fully offline mode using local LLMs (Ollama, LM Studio)
📄 License
This project is licensed under the MIT License.
MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
👥 Author & Acknowledgements
Author
Manu Ascendion
GitHub: @ManuAscendion
Acknowledgements
Library / Tool	Purpose
PyGithub	GitHub API wrapper for Python
Google Flan-T5	Local AI model for natural language intent detection
SpeechRecognition	Voice input processing
pyttsx3	Offline text-to-speech engine
AWS Bedrock (Claude 3 Sonnet)	Cloud LLM backend for deep code analysis
LangChain	Text splitting and LLM integration
ReportLab	Professional PDF generation
python-pptx	PowerPoint presentation generation
Google Gemini	Answer generation for RAG chatbot
FAISS	Fast similarity search for vector retrieval
SentenceTransformers	Text embedding model (all-MiniLM-L6-v2)
Streamlit	Interactive web UI for the RAG chatbot
FPDF	Chat session PDF export
PyPDF	PDF text extraction from within repositories
<div align="center">
Built with 🎙️ voice, ☁️ cloud, and 🤖 AI
⬆ Back to Top
</div>
