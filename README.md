🚀 Intelligent GitHub Automation Suite

Voice-Controlled Repository Creation → AI-Powered Repository Analysis → RAG-Based Q&A Chatbot

An end-to-end AI automation pipeline that transforms a spoken GitHub command into a fully analyzed, documented, and queryable repository ecosystem.

📌 Table of Contents


Project Overview


System Architecture


Pipeline Workflow


System 1 — GitHub Voice Assistant


System 2 — Repository Analyzer


System 3 — RAG-Based Q&A Chatbot


Repository Link Distribution


Tech Stack


Project Structure


Installation & Setup


Usage Guide


Voice Commands Reference


Configuration


Deployment Considerations


Troubleshooting


Security


Performance Reference


Contributing


License


Acknowledgements



🧠 Project Overview
The Intelligent GitHub Automation Suite is a multi-system AI platform that automates the entire lifecycle of GitHub repository management, documentation, and knowledge extraction.
This platform combines three independently designed AI systems into a unified workflow:
🔹 System 1 — GitHub Voice Assistant
A voice-controlled GitHub automation tool that creates repositories, manages branches, pull requests, collaborators, issues, and workflows using natural language voice commands.
🔹 System 2 — Repository Analyzer
An AI-powered repository analysis engine that downloads GitHub repositories, performs deep file-level and architecture-level analysis using LLMs, and generates professional PDF reports and PowerPoint presentations.
🔹 System 3 — RAG-Based Q&A Chatbot
A Retrieval-Augmented Generation chatbot built using FAISS + embeddings + Gemini that enables users to ask contextual questions about any GitHub repository and export conversations as structured PDFs.
Once a repository is created through System 1, the generated GitHub repository URL is distributed to System 2 and System 3 using a CURL-based endpoint architecture for independent parallel processing.

🏗️ System Architecture
┌──────────────────────────────────────────────────────────────┐│                    USER (Local Machine)                      ││                                                              ││   🎙️ Voice Command → GitHub Voice Assistant                  ││                                                              ││        ↓                                                     ││   Repository Created & Code Pushed                           ││                                                              ││        ↓                                                     ││   GitHub Repository URL Generated                            ││                                                              ││        ↓                                                     ││   CURL POST Request Sent to Remote Endpoint                  │└────────────────────────┬─────────────────────────────────────┘                         │              ┌──────────┴──────────┐              │                     │              ▼                     ▼┌─────────────────────┐   ┌─────────────────────────────────┐│    ☁️ CLOUD VM A    │   │         ☁️ CLOUD VM B            ││                     │   │                                  ││  System 2           │   │  System 3                        ││  Repository Analyzer│   │  RAG Q&A Chatbot                ││                     │   │                                  ││  • Repo Download    │   │  • Repo Download                 ││  • File Parsing     │   │  • Embedding Generation          ││  • Chunk Analysis   │   │  • FAISS Vector Store            ││  • PDF Generation   │   │  • Gemini Q&A                    ││  • PPT Generation   │   │  • Chat PDF Export               │└─────────────────────┘   └─────────────────────────────────┘

🔄 Pipeline Workflow
Step 1 — Voice-Controlled Repository Creation


User launches the Voice Assistant


User speaks a natural language command


Speech recognition converts voice → text


Flan-T5 interprets the intent


GitHub API creates repository


Local project is committed and pushed


GitHub repository URL is generated



Step 2 — Repository URL Distribution
A CURL request sends the repository URL to a remote endpoint:
curl -X POST "http://<endpoint>/receive" \  -H "Content-Type: application/json" \  -d '{"link": "https://github.com/<owner>/<repo>"}'
The endpoint forwards the repository link to:


☁️ Cloud VM A → System 2


☁️ Cloud VM B → System 3


Both systems process the repository independently and concurrently.

Step 3 — System 2 Processing
System 2:


Downloads repository ZIP


Extracts repository files


Filters supported file types


Splits code into chunks


Performs LLM-based analysis


Generates:


PDF report


PowerPoint presentation


Structured analysis summary





Step 4 — System 3 Processing
System 3:


Downloads repository


Extracts repository text


Generates embeddings


Builds FAISS vector database


Enables contextual repository Q&A


Exports full chat history as PDF



🎙️ System 1 — GitHub Voice Assistant
📌 Overview
A voice-controlled GitHub management assistant powered by:


Google Speech Recognition


Flan-T5


PyGithub


pyttsx3


Supports both voice and text input modes.

✅ Core Features
CategoryFeaturesRepository ManagementCreate, delete, push, pull repositoriesCollaborationAdd/remove collaboratorsIssuesCreate, comment, close issuesPull RequestsCreate, merge, list PRsBranchingCreate/delete/list branchesGitHub ActionsCreate workflow templatesInput ModesVoice mode + Text mode

⚙️ Technical Flow
Voice Input    ↓Speech Recognition    ↓Flan-T5 Intent Detection    ↓Command Parser    ↓GitHub API / Git Commands    ↓Text-to-Speech Response

📊 System 2 — Repository Analyzer
📌 Overview
An automated repository analysis engine powered by:


AWS Bedrock


Claude 3 Sonnet


LangChain


ReportLab


python-pptx



✅ Functional Capabilities


Repository ZIP download


File filtering & extraction


Recursive chunking


LLM-based code analysis


PDF report generation


PPT presentation generation



📑 Report Sections Generated
#Section1Project Summary2Tech Stack3File Structure4Core Modules5Data Flow6Code Quality7Red Flags8Security Risks9Performance Risks10Refactor Suggestions

📄 PDF Features


Structured layout


Tech stack tables


Security highlights


Warning boxes


Professional formatting



📊 PPT Features


Gradient title slide


Auto-pagination


Section slides


Warning-styled risk slides


Architecture visuals



💬 System 3 — RAG-Based Q&A Chatbot
📌 Overview
A Retrieval-Augmented Generation chatbot using:


FAISS


Gemini


SentenceTransformers


Streamlit


Enables contextual repository understanding through semantic retrieval.

✅ Core Capabilities
Retrieval Pipeline


Repository download


Text extraction


Semantic chunking


Embedding generation


FAISS vector indexing


Chat Interface


Natural language Q&A


Context-aware responses


Session memory


Multi-step explanations


PDF Export
Exports:


Questions


Answers


Detailed explanations


Timestamps


Repository metadata



📡 Repository Link Distribution
curl -X POST "http://<your-endpoint>/receive" \  -H "Content-Type: application/json" \  -d '{"link": "https://github.com/<owner>/<repo>"}'
Endpoint Responsibilities


Receives repository link


Triggers System 2


Triggers System 3


Enables parallel execution



🛠️ Tech Stack
🎙️ System 1 — Voice Assistant
ComponentTechnologyLanguagePythonAI ModelGoogle Flan-T5Speech RecognitionSpeechRecognitionGitHub IntegrationPyGithubTTSpyttsx3NLPHuggingFace Transformers

📊 System 2 — Repository Analyzer
ComponentTechnologyLLMClaude 3 SonnetCloud PlatformAWS BedrockChunkingLangChainPDF GenerationReportLabPPT Generationpython-pptx

💬 System 3 — RAG Chatbot
ComponentTechnologyUIStreamlitLLMGemini 2.5 FlashEmbeddingsall-MiniLM-L6-v2Vector StoreFAISSPDF ExportFPDF

📁 Project Structure
intelligent-github-suite/├── system1_voice_assistant/│   ├── main.py│   ├── requirements.txt│   ├── .env.example│   └── .github/workflows/├── system2_repo_analyzer/│   ├── integrated_github_analyzer.py│   ├── requirements.txt│   └── analysis_output/├── system3_rag_chatbot/│   ├── app.py│   ├── requirements.txt│   └── fonts/├── endpoint/│   └── receiver.py├── README.md└── architecture_workflow.pdf

⚙️ Installation & Setup
📌 Prerequisites


Python 3.9+


GitHub Personal Access Token


AWS Bedrock access


Gemini API key


Microphone (optional)


Cloud VMs



🎙️ System 1 Setup
git clone https://github.com/YOUR_USERNAME/intelligent-github-suite.gitcd intelligent-github-suite/system1_voice_assistantpython -m venv venv# Windowsvenv\Scripts\activate# Linux / Macsource venv/bin/activatepip install -r requirements.txt
Configure .env
GITHUB_TOKEN=your_tokenGITHUB_USERNAME=your_username

📊 System 2 Setup
cd system2_repo_analyzerpip install -r requirements.txt
Configure AWS
AWS_CONFIG = {    "access_key": "YOUR_KEY",    "secret_key": "YOUR_SECRET",    "region": "us-east-1",    "model_id": "anthropic.claude-3-sonnet"}

💬 System 3 Setup
cd system3_rag_chatbotpip install -r requirements.txt
Configure .env
GENAI_API_KEY=your_api_key

🚀 Usage Guide
Run System 1
python main.py

Run System 2
python integrated_github_analyzer.py

Run System 3
streamlit run app.py

🗣️ Voice Commands Reference
Repository Operations
Create repository <name>Delete repository <name>Push to <repo-name>Pull from <repo-name>

Issue Management
Create issue titled "<title>"Close issue <number>List issues

Pull Requests
Create pull requestMerge pull requestList pull requests

Branch Operations
Create branch <name>Delete branch <name>List branches

🔧 Configuration
Customize Voice Speed
engine.setProperty('rate', 150)

Customize Speech Timeout
def listen_command(timeout=6, phrase_time_limit=8):

Use Larger Flan-T5 Model
google/flan-t5-base

☁️ Deployment Considerations
Recommended VM Specifications
SystemRecommended SpecsSystem 24+ vCPUs, 8GB+ RAMSystem 32+ vCPUs, 4GB+ RAM

Security Recommendations


Store secrets in .env


Use IAM roles


Never hardcode API keys


Use cloud secret managers



🐛 Troubleshooting
ProblemSolutionMicrophone not workingReinstall PyAudioGitHub token invalidRegenerate tokenStreamlit not loadingChange portEmbedding failuresInstall compatible FAISS version

🛡️ Security
✅ Best Practices


Use Personal Access Tokens


Rotate credentials regularly


Use .gitignore


Avoid committing secrets


Use fine-grained access scopes



📊 Performance Reference
OperationApproximate TimeVoice recognition1–2 secFlan-T5 inference0.5–1 secRepository analysis10–25 minFAISS indexing30–120 secGemini answer generation3–8 sec

🤝 Contributing
Contribution Steps
git checkout -b feature/your-feature-namegit commit -m "Add your feature"git push origin feature/your-feature-name

Future Improvements


Hybrid search


Private repo support


Slack/Discord integration


Mobile voice app


Multi-repo analytics dashboard


Offline LLM support



📄 License
This project is licensed under the MIT License.

🙌 Acknowledgements
ToolPurposePyGithubGitHub API integrationFlan-T5Intent detectionLangChainText chunkingAWS BedrockRepository analysisGeminiQ&A generationFAISSVector searchStreamlitWeb UI

<div align="center">
Built with 🎙️ Voice + ☁️ Cloud + 🤖 AI
⭐ If you found this project useful, consider giving it a star!
</div>
Source 
