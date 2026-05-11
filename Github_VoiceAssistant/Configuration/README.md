# 🎙️ GitHub Voice Assistant

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![GitHub API](https://img.shields.io/badge/GitHub-API-black.svg)
![AI](https://img.shields.io/badge/AI-Flan--T5-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Voice-controlled GitHub repository management powered by AI**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Commands](#-commands) • [Demo](#-demo)

</div>

---

## 📖 Overview

GitHub Voice Assistant is an intelligent, voice-controlled command-line tool that lets you manage GitHub repositories, issues, pull requests, and workflows using natural language commands. Powered by Google's Flan-T5 AI model, it understands context and can execute complex GitHub operations hands-free.

### Why This Tool?

- 🎤 **Voice Control**: Execute GitHub operations without typing
- 🤖 **AI-Powered**: Natural language understanding via Flan-T5
- 🔒 **Secure**: Token-based authentication, credentials never hardcoded
- ⚡ **Fast**: Local AI processing for quick responses
- 🎯 **Comprehensive**: Manage repos, issues, PRs, branches, and workflows

---

## ✨ Features

### 🗂️ Repository Management
- ✅ Create new repositories (public/private)
- ✅ Delete repositories (with safety confirmations)
- ✅ Push local folders to GitHub
- ✅ Pull latest changes from remote
- ✅ Auto-generate `.gitignore` files

### 👥 Collaboration
- ✅ Add/remove collaborators
- ✅ Set permissions (read, write, admin)
- ✅ Manage team access

### 🐛 Issue Tracking
- ✅ Create issues with titles and descriptions
- ✅ List open/closed issues
- ✅ Comment on issues
- ✅ Close issues

### 🔀 Pull Requests
- ✅ Create pull requests between branches
- ✅ List open/merged PRs
- ✅ Merge pull requests
- ✅ Comment on pull requests

### 🌿 Branch Management
- ✅ Create new branches from any base
- ✅ List all branches
- ✅ Delete branches

### ⚙️ GitHub Actions
- ✅ Create workflow templates (Python tests, deployment)
- ✅ Check workflow status
- ✅ View build results

### 🎙️ Dual Input Modes
- ✅ **Voice Mode**: Speak commands naturally
- ✅ **Text Mode**: Type commands (auto-fallback if no mic)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│          User Input (Voice/Text)            │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Speech Recognition  │
        │   (Google API)       │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   Flan-T5 AI Model   │
        │  Natural Language    │
        │   Understanding      │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Command Parser      │
        │  Intent Detection    │
        └──────────┬───────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
    ┌─────────┐       ┌─────────┐
    │ GitHub  │       │   Git   │
    │   API   │       │ Commands│
    └─────────┘       └─────────┘
          │                 │
          └────────┬────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │    Text-to-Speech    │
        │  (pyttsx3 Engine)    │
        └──────────────────────┘
```

---

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **GitHub Account**: Personal Access Token required
- **Microphone**: For voice mode (optional)
- **OS**: Windows, Linux, or macOS

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/github-voice-assistant.git
cd github-voice-assistant
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: First installation downloads ~300MB AI model (Flan-T5-small)

### Step 4: Install PyAudio (Voice Mode)

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### Step 5: Configure Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env  # or use any text editor
```

**Required values:**
```bash
GITHUB_TOKEN=ghp_your_token_here
GITHUB_USERNAME=YourGitHubUsername
```

**Get your GitHub token:**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`, `admin:org`
4. Copy and paste into `.env`

---

## 💻 Usage

### Launch the Assistant

```bash
python main.py
```

### Choose Input Mode

```
🎤 Choose input mode — Voice (v) or Text (t) [auto fallback]: v
```

- **Type `v`**: Voice mode (requires microphone)
- **Type `t`**: Text mode (keyboard input)
- **Auto-fallback**: If mic fails, switches to text mode

---

## 🗣️ Voice Commands

### Repository Operations

```bash
# Create repository
"Create repository my-new-project"
"Create repo test-app"

# Delete repository (requires confirmation)
"Delete repository old-project"

# Push local folder
"Push to my-repo"
"Push folder to test-project"

# Pull changes
"Pull from my-repo"
"Pull repository updates"
```

### Issue Management

```bash
# Create issue
"Create issue titled 'Bug in login' in repository my-app"

# List issues
"List issues in repository my-app"

# Comment on issue
"Comment 'This is fixed' on issue 5 in repository my-app"

# Close issue
"Close issue 3 in repository my-app"
```

### Pull Requests

```bash
# Create PR
"Create pull request titled 'Add new feature' from feature-branch to main in repository my-app"

# List PRs
"List pull requests in repository my-app"

# Merge PR
"Merge pull request 7 in repository my-app"

# Comment on PR
"Comment 'Looks good' on pull request 4 in repository my-app"
```

### Branch Operations

```bash
# Create branch
"Create branch feature-login from main in repository my-app"

# List branches
"List branches in repository my-app"

# Delete branch
"Delete branch old-feature in repository my-app"
```

### Collaborators

```bash
# Add collaborator
"Add collaborator john-doe to repository my-app"

# The assistant will ask for permission level:
# "What level of access should I give — read, write, or admin?"
```

### GitHub Actions

```bash
# Create workflow
"Create action in repository my-app"

# Check workflow status
"Check workflow in repository my-app"
```

---

## ⌨️ Text Commands

Same commands as voice, just type them:

```bash
💬 Type your command: create repository my-test-repo
💬 Type your command: push to my-repo
💬 Type your command: list issues in repository my-app
```

---

## 📁 Project Structure

```
github-voice-assistant/
│
├── main.py                          # Main application file
│
├── 📂 push/                         # Staging folder for uploads
│   └── (your files to push)
│
├── 📂 local_repo/                   # Cloned repositories
│   └── (cloned repos appear here)
│
├── 📂 .github/
│   └── workflows/
│       └── python-test.yml          # Auto-generated workflow
│
├── 📄 Configuration
│   ├── .env                         # Your credentials (NOT in repo)
│   ├── .env.example                 # Template
│   ├── .gitignore                   # Git ignore rules
│   └── requirements.txt             # Python dependencies
│
├── 📄 Documentation
│   ├── README.md                    # This file
│   ├── Images&Scene_Detection_AGENTS.pdf
│   └── IRIS Medical Coding Agent.docx
│
└── 📄 Runtime Files (ignored)
    ├── current_repo.txt             # Tracks active repo
    └── venv/                        # Virtual environment
```

---

## 🛡️ Security

### Best Practices

✅ **Token Security**
- Never commit `.env` file
- Use Personal Access Tokens (not password)
- Rotate tokens regularly

✅ **Permission Scopes**
- Only grant necessary scopes
- Use fine-grained tokens when possible

✅ **Auto-Cleanup**
- Staging directories deleted after push
- No sensitive data left in temp files

### What's NOT Committed

The `.gitignore` automatically excludes:
- ❌ `.env` (your GitHub token)
- ❌ `venv/` (virtual environment)
- ❌ `push/` (staging folder)
- ❌ `local_repo/` (cloned repos)
- ❌ `current_repo.txt` (runtime state)
- ❌ `__pycache__/` (Python cache)

---

## 🔧 Configuration

### Customize Voice Settings

Edit in `main.py`:

```python
# TTS voice speed
engine.setProperty('rate', 150)  # Words per minute

# TTS volume
engine.setProperty('volume', 1.0)  # 0.0 to 1.0
```

### Customize Speech Recognition

```python
# Timeout settings
def listen_command(timeout=6, phrase_time_limit=8):
    # Adjust these values based on your speaking speed
```

### Change AI Model

```python
# Use larger model for better understanding
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Microphone unavailable"
```bash
Solution: Install PyAudio properly for your OS
Windows: pipwin install pyaudio
Mac: brew install portaudio && pip install pyaudio
Linux: sudo apt-get install portaudio19-dev
```

**Issue**: "GitHub token invalid"
```bash
Solution: 
1. Check token in .env file
2. Verify scopes: repo, workflow, admin:org
3. Regenerate token if expired
```

**Issue**: "Could not understand audio"
```bash
Solution:
1. Speak clearly near microphone
2. Reduce background noise
3. Try text mode instead (type 't')
```

**Issue**: "Model download fails"
```bash
Solution:
1. Check internet connection
2. Clear Hugging Face cache: rm -rf ~/.cache/huggingface
3. Retry installation
```

---

## 📊 Performance

| Operation | Avg Time | Notes |
|-----------|----------|-------|
| Voice Recognition | 1-2s | Depends on speech clarity |
| AI Processing | 0.5-1s | Local Flan-T5 inference |
| GitHub API Call | 0.5-2s | Depends on network |
| Push to GitHub | 3-10s | Depends on folder size |

---

## 🗺️ Roadmap

### Version 2.0
- [ ] Multi-repository operations
- [ ] Batch issue creation from CSV
- [ ] Advanced workflow templates
- [ ] GitHub Organizations support
- [ ] Custom voice commands configuration

### Version 3.0
- [ ] Web interface (Streamlit)
- [ ] Mobile app (iOS/Android)
- [ ] Slack/Discord integration
- [ ] Team analytics dashboard

---

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Author

**Manu Ascendion**
- GitHub: [@ManuAscendion](https://github.com/ManuAscendion)

---

## 🙏 Acknowledgments

- **PyGithub** - GitHub API wrapper
- **Google Flan-T5** - Natural language AI model
- **SpeechRecognition** - Voice input library
- **pyttsx3** - Text-to-speech engine

---

## 📞 Support

### Issues
Report bugs: [GitHub Issues](https://github.com/YOUR_USERNAME/github-voice-assistant/issues)

### Documentation
Full docs: [Wiki](https://github.com/YOUR_USERNAME/github-voice-assistant/wiki)

---

<div align="center">

**Built with 🎙️ by Manu Ascendion**

[⬆ Back to Top](#-github-voice-assistant)

</div>