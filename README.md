<div align="center">

# 🚀 Intelligent GitHub Automation Suite

### 🎙️ Voice-Controlled Repository Creation  
### 📊 AI-Powered Repository Analysis  
### 💬 RAG-Based Repository Q&A Chatbot

<p align="center">
An end-to-end AI automation ecosystem that transforms spoken GitHub commands into fully analyzed, documented, and queryable repositories.
</p>

<br>

<img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/AWS-Bedrock-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>
<img src="https://img.shields.io/badge/Google-Gemini-EA4335?style=for-the-badge&logo=google&logoColor=white"/>
<img src="https://img.shields.io/badge/VectorDB-FAISS-009688?style=for-the-badge"/>
<img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<br><br>

<img src="https://img.shields.io/github/stars/YOUR_USERNAME/intelligent-github-suite?style=social"/>
<img src="https://img.shields.io/github/forks/YOUR_USERNAME/intelligent-github-suite?style=social"/>
<img src="https://img.shields.io/github/license/YOUR_USERNAME/intelligent-github-suite"/>

</div>

---

# 📌 Overview

The **Intelligent GitHub Automation Suite** is a multi-system AI platform designed to automate the complete lifecycle of:

- ✅ GitHub Repository Management  
- ✅ AI-Powered Repository Analysis  
- ✅ Knowledge Extraction & Semantic Search  
- ✅ Documentation Generation  
- ✅ Retrieval-Augmented Q&A  

This project combines **three independently designed AI systems** into one seamless automation workflow.

---

# ⚡ Systems Included

| System | Description |
|:---|:---|
| 🎙️ **System 1** | Voice-controlled GitHub automation assistant |
| 📊 **System 2** | AI-powered repository analyzer & documentation engine |
| 💬 **System 3** | RAG-based GitHub repository Q&A chatbot |

---

# 🏗️ System Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                    USER (Local Machine)                      │
│                                                              │
│   🎙️ Voice Command → GitHub Voice Assistant                  │
│                                                              │
│        ↓                                                     │
│   Repository Created & Code Pushed                           │
│                                                              │
│        ↓                                                     │
│   GitHub Repository URL Generated                            │
│                                                              │
│        ↓                                                     │
│   CURL POST Request Sent to Remote Endpoint                  │
└────────────────────────┬─────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼

┌─────────────────────┐   ┌─────────────────────────────────┐
│    ☁️ CLOUD VM A    │   │         ☁️ CLOUD VM B            │
│                     │   │                                  │
│  📊 System 2        │   │  💬 System 3                     │
│  Repo Analyzer      │   │  RAG Q&A Chatbot                │
│                     │   │                                  │
│  • Repo Download    │   │  • Embedding Generation          │
│  • File Parsing     │   │  • FAISS Vector DB               │
│  • LLM Analysis     │   │  • Gemini Responses              │
│  • PDF/PPT Output   │   │  • PDF Chat Export               │
└─────────────────────┘   └─────────────────────────────────┘
```

---

# 🔄 Complete Workflow

## 🎙️ Step 1 — Voice-Based GitHub Automation

The user launches the Voice Assistant and speaks commands such as:

```bash
Create repository AI-Automation-Suite
```

### The system automatically performs:

- 🎤 Speech-to-text conversion  
- 🧠 Intent recognition using Flan-T5  
- 🔗 GitHub API execution  
- 📁 Local Git operations  
- 🚀 Automatic repository push  

---

## 📡 Step 2 — Repository Distribution

Once the repository is created, the repository URL is distributed using a CURL request:

```bash
curl -X POST "http://<endpoint>/receive" \
  -H "Content-Type: application/json" \
  -d '{"link":"https://github.com/<owner>/<repo>"}'
```

### The endpoint forwards the repository link to:

- ☁️ Cloud VM A → Repository Analyzer  
- ☁️ Cloud VM B → RAG Chatbot  

Both systems execute independently and concurrently.

---

# 🎙️ System 1 — GitHub Voice Assistant

## 📌 Description

A voice-controlled GitHub management assistant powered by:

- 🧠 Flan-T5
- 🎤 SpeechRecognition
- 🔗 PyGithub
- 🔊 pyttsx3

Supports both:

- 🎙️ Voice Mode  
- ⌨️ Text Mode  

---

## ✨ Features

### 📁 Repository Management

- Create repositories
- Delete repositories
- Push local folders
- Pull latest changes

### 👥 Collaboration

- Add collaborators
- Remove collaborators
- Assign permissions

### 🐛 Issue Management

- Create issues
- Comment on issues
- Close issues
- List issues

### 🔀 Pull Requests

- Create PRs
- Merge PRs
- List pull requests

### 🌿 Branch Management

- Create branches
- Delete branches
- List branches

### ⚙️ GitHub Actions

- Create workflow templates
- Check workflow status

---

## ⚙️ Technical Flow

```text
Voice Input
    ↓
Speech Recognition
    ↓
Flan-T5 Intent Detection
    ↓
Command Parser
    ↓
GitHub API / Git Commands
    ↓
Text-to-Speech Response
```

---

# 📊 System 2 — Repository Analyzer

## 📌 Description

An automated AI-powered repository analysis engine that generates:

- 📄 Professional PDF Reports  
- 📊 PowerPoint Presentations  
- 🧠 Architecture Summaries  

Powered by:

- AWS Bedrock  
- Claude 3 Sonnet  
- LangChain  

---

## ✨ Core Features

### 📥 Repository Processing

- ZIP download
- Branch fallback (`main → master`)
- File extraction
- Directory filtering

### 🧠 AI Analysis

- Recursive text chunking
- Per-file analysis
- Architecture understanding
- Security & performance review

### 📄 Report Generation

- PDF report generation
- PowerPoint slide generation
- Structured project summaries

---

## 📑 Report Sections

| # | Section |
|---|---|
| 1 | Project Summary |
| 2 | Tech Stack |
| 3 | File Structure |
| 4 | Core Modules |
| 5 | Data Flow |
| 6 | Code Quality |
| 7 | Security Risks |
| 8 | Performance Risks |
| 9 | Refactor Suggestions |
| 10 | Architecture Summary |

---

# 💬 System 3 — RAG-Based Q&A Chatbot

## 📌 Description

A Retrieval-Augmented Generation chatbot that enables users to ask natural language questions about any GitHub repository.

Built using:

- 🧠 Gemini  
- 📚 FAISS  
- 🔍 SentenceTransformers  
- 🎨 Streamlit  

---

## ✨ Features

### 📚 Semantic Retrieval

- Repository parsing
- Embedding generation
- FAISS vector indexing
- Context retrieval

### 💬 Interactive Chat

- Repository Q&A
- Context-aware responses
- Detailed explanations
- Session memory

### 📄 PDF Export

- Export complete conversations
- Structured knowledge reports
- Downloadable documentation

---

# 🛠️ Tech Stack

## 🎙️ System 1 — Voice Assistant

| Category | Technology |
|---|---|
| Language | Python |
| AI Model | Flan-T5 |
| Speech Recognition | SpeechRecognition |
| GitHub Integration | PyGithub |
| Text-to-Speech | pyttsx3 |
| NLP | HuggingFace Transformers |

---

## 📊 System 2 — Repository Analyzer

| Category | Technology |
|---|---|
| LLM | Claude 3 Sonnet |
| Cloud Platform | AWS Bedrock |
| Framework | LangChain |
| PDF Generation | ReportLab |
| PPT Generation | python-pptx |

---

## 💬 System 3 — RAG Chatbot

| Category | Technology |
|---|---|
| UI Framework | Streamlit |
| LLM | Gemini 2.5 Flash |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| PDF Export | FPDF |

---

# 📁 Project Structure

```text
intelligent-github-suite/
│
├── 📂 system1_voice_assistant/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .github/workflows/
│
├── 📂 system2_repo_analyzer/
│   ├── integrated_github_analyzer.py
│   ├── requirements.txt
│   └── analysis_output/
│
├── 📂 system3_rag_chatbot/
│   ├── app.py
│   ├── requirements.txt
│   └── fonts/
│
├── 📂 endpoint/
│   └── receiver.py
│
├── README.md
└── architecture_workflow.pdf
```

---

# ⚙️ Installation

## 📌 Prerequisites

- Python 3.9+
- GitHub Personal Access Token
- AWS Bedrock Access
- Gemini API Key
- Cloud VMs (Optional)

---

## 🎙️ System 1 Setup

```bash
git clone https://github.com/YOUR_USERNAME/intelligent-github-suite.git

cd intelligent-github-suite/system1_voice_assistant

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Configure `.env`

```env
GITHUB_TOKEN=your_token
GITHUB_USERNAME=your_username
```

---

## 📊 System 2 Setup

```bash
cd system2_repo_analyzer

pip install -r requirements.txt
```

---

## 💬 System 3 Setup

```bash
cd system3_rag_chatbot

pip install -r requirements.txt
```

### Configure `.env`

```env
GENAI_API_KEY=your_api_key
```

---

# 🚀 Running the Systems

## 🎙️ Run Voice Assistant

```bash
python main.py
```

---

## 📊 Run Repository Analyzer

```bash
python integrated_github_analyzer.py
```

---

## 💬 Run RAG Chatbot

```bash
streamlit run app.py
```

---

# 🗣️ Voice Commands

## 📁 Repository Commands

```bash
Create repository <name>
Delete repository <name>
Push to <repo-name>
Pull from <repo-name>
```

---

## 🐛 Issue Commands

```bash
Create issue titled "<title>"
Close issue <number>
List issues
```

---

## 🔀 Pull Request Commands

```bash
Create pull request
Merge pull request
List pull requests
```

---

## 🌿 Branch Commands

```bash
Create branch <name>
Delete branch <name>
List branches
```

---

# ☁️ Deployment Considerations

| System | Recommended Specs |
|---|---|
| 📊 System 2 | 4+ vCPUs, 8GB+ RAM |
| 💬 System 3 | 2+ vCPUs, 4GB+ RAM |

---

# 🛡️ Security Best Practices

✅ Store credentials in `.env` files  
✅ Use IAM roles or secret managers  
✅ Never commit API keys  
✅ Use fine-grained GitHub tokens  
✅ Rotate credentials regularly  

---

# 📊 Performance Reference

| Operation | Approximate Time |
|---|---|
| 🎤 Voice Recognition | 1–2 sec |
| 🧠 Flan-T5 Inference | 0.5–1 sec |
| 📊 Repository Analysis | 10–25 min |
| 📚 FAISS Indexing | 30–120 sec |
| 💬 Gemini Response | 3–8 sec |

---

# 🤝 Contributing

```bash
git checkout -b feature/your-feature-name

git commit -m "Add your feature"

git push origin feature/your-feature-name
```

---

# 📄 License

Licensed under the **MIT License**

---

# 🙌 Acknowledgements

- PyGithub
- Flan-T5
- AWS Bedrock
- Claude 3 Sonnet
- LangChain
- Streamlit
- Gemini
- FAISS
- ReportLab
- python-pptx

---

<div align="center">

# ⭐ Built with Voice + Cloud + AI

### If you found this project useful, consider giving it a star ⭐

</div>
