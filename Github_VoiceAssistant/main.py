# main.py — Secure Voice-driven GitHub Assistant
# Features:
#  - Voice or Text mode selection
#  - Repo creation, folder push (from /push only)
#  - Collaborator management
#  - Issue management (create, list, comment, close)
#  - Auto .gitignore management & safe cleanup

import os, ssl, requests, subprocess, shutil, json, atexit, stat
from pathlib import Path
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
from github import Github
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# ====== SSL / HF bypass (for Hugging Face on Windows) ======
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['HF_HUB_OFFLINE'] = '0'
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''
ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()
# ============================================================

# ------------------ TTS setup ------------------
engine = pyttsx3.init()
@atexit.register
def cleanup_tts():
    try:
        engine.stop()
    except Exception:
        pass
# ------------------------------------------------

# ------------------ ENV & GitHub -----------------
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME") or "ManuAscendion"

if not GITHUB_TOKEN:
    raise SystemExit("❌ Please set GITHUB_TOKEN in your .env file.")

gh = Github(GITHUB_TOKEN)
# -------------------------------------------------

# ------------------ MODEL LOAD -------------------
print("🧠 Loading Flan-T5 model... (first time may take a bit)")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small", trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small", trust_remote_code=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print("✅ Model loaded!\n")
# -------------------------------------------------

CURRENT_REPO_FILE = Path("current_repo.txt")
WORKDIR = Path.cwd()
PUSH_FOLDER = WORKDIR / "push"

# ------------------ SPEECH ------------------------
def speak(text):
    print("SPEAK:", text)
    engine.say(text)
    engine.runAndWait()
# -------------------------------------------------
def listen_command(timeout=6, phrase_time_limit=8):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as src:
            print("🎧 Listening... Say your command:")
            r.adjust_for_ambient_noise(src, duration=0.5)
            try:
                audio = r.listen(src, timeout=timeout, phrase_time_limit=phrase_time_limit)
            except Exception as e:
                print("❌ Listen timeout:", e)
                return None
    except Exception as e:
        print("⚠️ Microphone unavailable:", e)
        return None  # <-- VERY IMPORTANT
    try:
        text = r.recognize_google(audio)
        print("🗣️ You said:", text)
        return text.strip()
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return None
    except sr.RequestError as e:
        print("❌ Speech service error:", e)
        return None


# ------------------ MEMORY HELPERS ----------------
def save_current_repo(name: str):
    try:
        CURRENT_REPO_FILE.write_text(name)
    except Exception:
        pass

def load_current_repo():
    if CURRENT_REPO_FILE.exists():
        try:
            return CURRENT_REPO_FILE.read_text().strip()
        except Exception:
            return None
    return None
# ---------------------------------------------------

# ------------------ AUTO .GITIGNORE ----------------
def ensure_gitignore():
    gitignore_content = """# --- 🧠 Environment & Secrets ---
.env
*.env

# --- 🐍 Python cache & build files ---
__pycache__/
*.py[cod]
*$py.class
*.pyo
*.pyd
*.egg-info/
build/
dist/

# --- 🧩 Virtual environments ---
venv/
.venv/
env/
ENV/
pip-wheel-metadata/

# --- ⚙️ IDE / Editor files ---
.vscode/
.idea/
*.swp
.DS_Store

# --- 🪄 Logs & runtime files ---
*.log
*.tmp
*.bak

# --- 🧰 Project-specific files ---
current_repo.txt
push/
"""
    path = WORKDIR / ".gitignore"
    path.write_text(gitignore_content, encoding="utf-8")
    print("✅ .gitignore verified/updated.")
# ---------------------------------------------------

# ------------------ GIT HELPERS --------------------
def run_cmd(cmd: str, cwd: Path = None):
    print("CMD >", cmd)
    try:
        res = subprocess.run(cmd, cwd=str(cwd) if cwd else None, shell=True,
                             check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(res.stdout)
        return True, res.stdout
    except subprocess.CalledProcessError as e:
        print("CMD error:", e.stderr or e)
        return False, e.stderr or str(e)

def ensure_git_initialized(cwd: Path):
    if (cwd / ".git").exists():
        return True
    ok, _ = run_cmd("git init", cwd)
    return ok

def force_delete(path):
    def onerror(func, p, exc_info):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except Exception:
            pass
    if path.exists():
        shutil.rmtree(path, onerror=onerror)

def git_add_commit_push(repo_name: str, commit_message: str = "Voice assistant commit"):
    if not PUSH_FOLDER.exists():
        speak("The 'push' folder does not exist.")
        return

    if not any(PUSH_FOLDER.iterdir()):
        speak("The 'push' folder is empty.")
        return

    ensure_git_initialized(WORKDIR)
    staging_dir = WORKDIR.parent / "_staging_push"

    force_delete(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    for item in PUSH_FOLDER.iterdir():
        dest = staging_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('.git', 'venv', '__pycache__', '.env', '.DS_Store'))
        else:
            shutil.copy2(item, dest)

    os.chdir(staging_dir)
    gitignore_path = staging_dir / ".gitignore"
    gitignore_path.write_text(".env\nvenv/\n__pycache__/\n.git/\n*.pyc\n.DS_Store\n", encoding="utf-8")

    remote_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{repo_name}.git"
    run_cmd("git init", staging_dir)
    run_cmd("git add .", staging_dir)
    run_cmd(f'git commit -m "{commit_message}"', staging_dir)
    run_cmd("git branch -M main || true", staging_dir)
    run_cmd(f"git remote add origin \"{remote_url}\"", staging_dir)
    ok, _ = run_cmd("git push -u origin main --force", staging_dir)

    os.chdir(WORKDIR)
    try:
        force_delete(staging_dir)
    except Exception as e:
        print(f"⚠️ Could not fully delete staging dir: {e}")

    if ok:
        speak(f"Pushed contents of 'push' folder into repository '{repo_name}' successfully.")
    else:
        speak("Push failed. Check the terminal for details.")
# ---------------------------------------------------

# ------------------ GIT PULL ------------------------
def git_pull(repo_name):
    repo_name = repo_name.strip().replace("repository", "").replace("repo", "").strip()
    repo_dir = WORKDIR / "local_repo" / repo_name

    if not repo_dir.exists():
        speak(f"Cloning {repo_name} first, since it's not in local.")
        run_cmd(f'git clone https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{repo_name}.git "{repo_dir}"')
        return

    os.chdir(repo_dir)
    speak(f"Pulling latest changes from {repo_name}.")
    ok, output = run_cmd("git pull origin main", repo_dir)
    if ok:
        speak("✅ Repository updated successfully.")
    else:
        speak("❌ Pull failed. Check for merge conflicts or connectivity issues.")
# ----------------------------------------------------



# ------------------ GITHUB ACTIONS -----------------
def create_github_repo(repo_name, private=False):
    try:
        user = gh.get_user()
        repo = user.create_repo(repo_name, private=private)
        speak(f"Repository {repo_name} created.")
        save_current_repo(repo_name)
        return repo
    except Exception as e:
        print("❌ GitHub create error:", e)
        speak("Failed to create repository.")
        return None

def add_collaborator(repo_name, collaborator_username):
    try:
        repo = gh.get_user().get_repo(repo_name)
    except Exception:
        speak(f"Repository {repo_name} not found.")
        return

    speak("What level of access should I give — read, write, or admin?")
    print("👉 Type or say: read / write / admin")
    perm = listen_command() or input("Access level: ").strip().lower()

    permission_map = {"read": "pull", "write": "push", "admin": "admin"}
    perm = permission_map.get(perm, "pull")

    speak(f"Adding collaborator {collaborator_username} with {perm} access to {repo_name}.")
    try:
        repo.add_to_collaborators(collaborator_username, permission=perm)
        speak(f"✅ Invitation sent to {collaborator_username}.")
    except Exception as e:
        print("❌ Error adding collaborator:", e)
        speak("Failed to add collaborator. Check username or permissions.")
# ---------------------------------------------------
# ------------------ DELETE REPOSITORY -----------------
def delete_github_repo(repo_name):
    try:
        repo = gh.get_user().get_repo(repo_name)
    except Exception:
        speak(f"Repository {repo_name} not found.")
        return

    # 🔒 First confirmation
    speak(f"Are you sure you want to delete the repository {repo_name}? Type yes to continue.")
    confirm = input(f"⚠️ Confirm deletion of '{repo_name}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        speak("Deletion cancelled.")
        return

    # 🔒 Second confirmation
    speak("This action is permanent. Type DELETE to confirm.")
    confirm2 = input("Type 'DELETE' to permanently remove the repository: ").strip().upper()
    if confirm2 != "DELETE":
        speak("Deletion cancelled for safety.")
        return

    # ✅ Proceed with deletion
    try:
        repo.delete()
        speak(f"Repository {repo_name} has been deleted successfully.")
        print(f"✅ Repository '{repo_name}' deleted.")
    except Exception as e:
        print("❌ Error deleting repository:", e)
        speak("Failed to delete the repository. Check permissions or name.")
# -------------------------------------------------------

# ------------------ ISSUES MANAGEMENT ---------------
def create_issue(repo_name, title, body=None):
    try:
        repo = gh.get_user().get_repo(repo_name)
        issue = repo.create_issue(title=title, body=body or "")
        speak(f"✅ Issue #{issue.number} created successfully.")
    except Exception as e:
        print("❌ Error creating issue:", e)
        speak("Failed to create issue.")

def list_issues(repo_name):
    try:
        repo = gh.get_user().get_repo(repo_name)
        issues = repo.get_issues(state="open")
        if issues.totalCount == 0:
            speak("There are no open issues.")
        else:
            speak(f"There are {issues.totalCount} open issues:")
            for issue in issues:
                print(f"#{issue.number}: {issue.title}")
                speak(f"Issue {issue.number}: {issue.title}")
    except Exception as e:
        print("❌ Error listing issues:", e)
        speak("Failed to list issues.")

def comment_on_issue(repo_name, issue_number, comment):
    try:
        repo = gh.get_user().get_repo(repo_name)
        issue = repo.get_issue(number=int(issue_number))
        issue.create_comment(comment)
        speak(f"💬 Comment added to issue #{issue_number}.")
    except Exception as e:
        print("❌ Error commenting on issue:", e)
        speak("Failed to add comment.")

def close_issue(repo_name, issue_number):
    try:
        repo = gh.get_user().get_repo(repo_name)
        issue = repo.get_issue(number=int(issue_number))
        issue.edit(state="closed")
        speak(f"✅ Issue #{issue_number} closed successfully.")
    except Exception as e:
        print("❌ Error closing issue:", e)
        speak("Failed to close issue.")
# ---------------------------------------------------

# ------------------ PULL REQUEST MANAGEMENT -----------------
def create_pull_request(repo_name, title, head_branch, base_branch="main", body=""):
    """Create a pull request from one branch to another."""
    try:
        repo = gh.get_user().get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head_branch, base=base_branch)
        speak(f"✅ Pull request #{pr.number} created: {pr.title}")
    except Exception as e:
        print("❌ Error creating pull request:", e)
        speak("Failed to create pull request. Check branch names or permissions.")

def list_pull_requests(repo_name, state="open"):
    """List open, closed, or all pull requests."""
    try:
        repo = gh.get_user().get_repo(repo_name)
        pulls = repo.get_pulls(state=state)
        if pulls.totalCount == 0:
            speak(f"There are no {state} pull requests in {repo_name}.")
        else:
            speak(f"There are {pulls.totalCount} {state} pull requests in {repo_name}:")
            for pr in pulls:
                print(f"#{pr.number}: {pr.title} (from {pr.head.ref} → {pr.base.ref})")
                speak(f"Pull request {pr.number}: {pr.title}")
    except Exception as e:
        print("❌ Error listing pull requests:", e)
        speak("Failed to list pull requests.")

def merge_pull_request(repo_name, pr_number):
    """Merge a pull request."""
    try:
        repo = gh.get_user().get_repo(repo_name)
        pr = repo.get_pull(number=int(pr_number))
        if pr.is_merged():
            speak(f"Pull request #{pr_number} is already merged.")
            return
        pr.merge()
        speak(f"✅ Pull request #{pr_number} merged successfully.")
    except Exception as e:
        print("❌ Error merging pull request:", e)
        speak("Failed to merge pull request.")

def comment_on_pull_request(repo_name, pr_number, comment):
    """Add a comment on a pull request."""
    try:
        repo = gh.get_user().get_repo(repo_name)
        pr = repo.get_pull(number=int(pr_number))
        pr.create_issue_comment(comment)
        speak(f"💬 Comment added to pull request #{pr_number}.")
    except Exception as e:
        print("❌ Error commenting on pull request:", e)
        speak("Failed to comment on pull request.")
# --------------------------------------------------------------

# ------------------ BRANCH MANAGEMENT -----------------
def create_branch(repo_name, new_branch, base_branch="main"):
    """Create a new branch in a repository based on the base branch."""
    try:
        repo = gh.get_user().get_repo(repo_name)
        base = repo.get_branch(base_branch)
        repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=base.commit.sha)
        speak(f"✅ Branch '{new_branch}' created from '{base_branch}' in {repo_name}.")
    except Exception as e:
        print("❌ Error creating branch:", e)
        speak("Failed to create branch. Check if it already exists or if base branch name is correct.")

def list_branches(repo_name):
    """List all branches in a repository."""
    try:
        repo = gh.get_user().get_repo(repo_name)
        branches = repo.get_branches()
        speak(f"There are {branches.totalCount} branches in {repo_name}.")
        for b in branches:
            print(f"- {b.name}")
            speak(b.name)
    except Exception as e:
        print("❌ Error listing branches:", e)
        speak("Failed to list branches.")

def delete_branch(repo_name, branch_name):
    """Delete a branch from a repository."""
    try:
        repo = gh.get_user().get_repo(repo_name)
        ref = repo.get_git_ref(f"heads/{branch_name}")
        ref.delete()
        speak(f"🗑️ Branch '{branch_name}' deleted successfully from {repo_name}.")
    except Exception as e:
        print("❌ Error deleting branch:", e)
        speak("Failed to delete branch. Make sure it exists and you're allowed to delete it.")
# --------------------------------------------------------


# ------------------ WORKFLOW STATUS CHECK -----------------
def check_workflow_status(repo_name):
    try:
        repo = gh.get_user().get_repo(repo_name)
        workflows = repo.get_workflow_runs()

        if workflows.totalCount == 0:
            speak(f"There are no workflow runs in {repo_name}.")
            return

        latest = workflows[0]
        status = latest.status
        conclusion = latest.conclusion or "in progress"
        time = latest.created_at.strftime("%Y-%m-%d %H:%M:%S")

        if conclusion == "success":
            speak(f"✅ The latest workflow in {repo_name} succeeded at {time}.")
        elif conclusion == "failure":
            speak(f"❌ The latest workflow in {repo_name} failed.")
        else:
            speak(f"⚙️ The latest workflow in {repo_name} is {conclusion}.")
    except Exception as e:
        print("❌ Error checking workflow status:", e)
        speak("Failed to check workflow status.")
# -----------------------------------------------------------


# -------------------- github action management----------------------------

def create_github_action(repo_name, action_type="python-test"):
    """Creates a basic GitHub Actions workflow in the given repository, including push folder content."""
    try:
        repo = gh.get_user().get_repo(repo_name)
    except Exception:
        speak(f"Repository {repo_name} not found.")
        return

    speak(f"Creating a GitHub Action workflow for {repo_name}...")

    # Define simple workflow templates
    workflows = {
        "python-test": """name: Run Python Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt || echo 'No requirements.txt found'

      - name: Run tests
        run: pytest || echo 'No tests found'
""",

        "deploy-basic": """name: Deploy Project

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Example deploy step
        run: echo "Deploying project..."
"""
    }

    if action_type not in workflows:
        speak("Invalid action type. Using python-test workflow by default.")
        action_type = "python-test"

    # 🧩 Create a temporary folder that merges push content + workflow
    workflow_dir = WORKDIR.parent / "_temp_action_push"
    force_delete(workflow_dir)
    workflow_dir.mkdir(parents=True, exist_ok=True)

    # Copy all contents from /push into temp folder
    if PUSH_FOLDER.exists():
        for item in PUSH_FOLDER.iterdir():
            dest = workflow_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

    # Create workflow folder
    workflow_path = workflow_dir / ".github" / "workflows"
    workflow_path.mkdir(parents=True, exist_ok=True)

    # Write workflow file
    workflow_file = workflow_path / f"{action_type}.yml"
    workflow_file.write_text(workflows[action_type], encoding="utf-8")

    # Git push everything (code + workflow)
    os.chdir(workflow_dir)
    remote_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{repo_name}.git"
    run_cmd("git init", workflow_dir)
    run_cmd("git add .", workflow_dir)
    run_cmd(f'git commit -m "Add GitHub Action ({action_type}) with project files"', workflow_dir)
    run_cmd("git branch -M main || true", workflow_dir)
    run_cmd(f"git remote add origin \"{remote_url}\"", workflow_dir)
    ok, _ = run_cmd("git push -u origin main --force", workflow_dir)

    os.chdir(WORKDIR)
    force_delete(workflow_dir)

    if ok:
        speak(f"✅ GitHub Action '{action_type}' and project files pushed successfully to {repo_name}.")
    else:
        speak("Failed to push the workflow. Check terminal for details.")



# ------------------ MAIN ACTIONS -------------------
def action_push_folder(repo):
    repo = repo or load_current_repo()
    if not repo:
        speak("Please specify a repository name.")
        return
    repo = repo.strip()
    try:
        gh.get_user().get_repo(repo)
    except Exception:
        create_github_repo(repo)
    speak(f"Pushing the 'push' folder to repository {repo}.")
    git_add_commit_push(repo, "Voice assistant commit")
# ---------------------------------------------------

def parse_and_run_command(raw_text):
    if not raw_text:
        speak("I didn’t catch that.")
        return
    text = raw_text.lower()

    # ---- Issues (Priority first to prevent conflicts) ----
    if "create" in text and "issue" in text:
        title = None
        repo = None
        if "titled" in text:
            title = text.split("titled")[-1].split("in")[0].strip()
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        if not title:
            title = input("Issue title: ")
        if not repo:
            repo = load_current_repo() or input("Repository name: ")
        create_issue(repo, title)
        return

    elif "list issues" in text:
        repo = None
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        if not repo:
            repo = load_current_repo() or input("Repository name: ")
        list_issues(repo)
        return

    elif "comment" in text and "issue" in text:
        repo = None
        comment = None
        num = None
        if "comment" in text:
            parts = text.split("comment")[1]
            if "on issue" in parts:
                comment = parts.split("on issue")[0].strip().strip("'\"")
        if "on issue" in text:
            num = ''.join([c for c in text.split("on issue")[-1] if c.isdigit()])
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        if not repo:
            repo = load_current_repo() or input("Repository name: ")
        if not num:
            num = input("Issue number: ")
        if not comment:
            comment = input("Comment text: ")
        comment_on_issue(repo, num, comment)
        return

    elif "close" in text and "issue" in text:
        repo = None
        num = ''.join([c for c in text.split("issue")[-1] if c.isdigit()])
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        if not repo:
            repo = load_current_repo() or input("Repository name: ")
        if not num:
            num = input("Issue number: ")
        close_issue(repo, num)
        return
    
        # ---- Pull Request Commands ----
    elif "create" in text and "pull request" in text:
        repo = None
        title = None
        head = None
        base = "main"

        # Try to extract details from text
        if "titled" in text:
            title = text.split("titled")[-1].split("from")[0].strip()
        if "from" in text:
            head = text.split("from")[-1].split("to")[0].strip()
        if "to" in text:
            base = text.split("to")[-1].split("in")[0].strip()
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()

        if not repo:
            repo = load_current_repo() or input("Repository name: ").strip()
        if not head:
            head = input("Source branch (head): ").strip()
        if not base:
            base = input("Target branch (base): ").strip()
        if not title:
            title = input("Pull request title: ").strip()

        create_pull_request(repo, title, head, base)
        return

    elif "list" in text and "pull requests" in text:
        repo = None
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        if not repo:
            repo = load_current_repo() or input("Repository name: ").strip()
        list_pull_requests(repo)
        return

    elif "merge" in text and "pull request" in text:
        repo = None
        num = ''.join([c for c in text.split("pull request")[-1] if c.isdigit()])
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        if not repo:
            repo = load_current_repo() or input("Repository name: ").strip()
        if not num:
            num = input("Pull request number: ")
        merge_pull_request(repo, num)
        return

    elif "comment" in text and "pull request" in text:
        repo = None
        comment = None
        num = None
        if "comment" in text:
            parts = text.split("comment")[1]
            if "on pull request" in parts:
                comment = parts.split("on pull request")[0].strip().strip("'\"")
        if "on pull request" in text:
            num = ''.join([c for c in text.split("on pull request")[-1] if c.isdigit()])
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        if not repo:
            repo = load_current_repo() or input("Repository name: ")
        if not num:
            num = input("Pull request number: ")
        if not comment:
            comment = input("Comment text: ")
        comment_on_pull_request(repo, num, comment)
        return

        # ---- Branch Commands ----
        # ---- Branch Commands ----
    elif ("create" in text or "make" in text or "creates" in text) and ("branch" in text or "feature" in text):
        repo = None
        branch = None
        base = "main"

        # Extract branch name intelligently
        if "branch" in text:
            branch = text.split("branch")[-1].split("from")[0].split("in")[0].strip()
        elif "feature" in text:
            branch = text.split("feature")[-1].split("from")[0].split("in")[0].strip()
            branch = f"feature-{branch.replace('-', '').strip()}"
        elif "create" in text:
            branch = text.split("create")[-1].split("from")[0].split("in")[0].strip()

        # Extract base branch
        if "from" in text:
            base = text.split("from")[-1].split("in")[0].strip()
        else:
            base = "main"

        # Extract repository
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        elif "in repo" in text:
            repo = text.split("in repo")[-1].strip()

        # If not said, ask manually
        if not repo:
            repo = load_current_repo() or input("Repository name: ").strip()
        if not branch:
            branch = input("Branch name: ").strip()
        if not base:
            base = "main"

        branch = branch.replace("repository", "").replace("repo", "").strip()
        repo = repo.replace("repository", "").replace("repo", "").strip()

        create_branch(repo, branch, base)
        return



        # ---- GitHub Actions ----
    elif "create" in text and "action" in text:
        repo = None
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        if not repo:
            repo = load_current_repo() or input("Repository name: ").strip()
        create_github_action(repo)
        return

    elif "check" in text and "workflow" in text:
        repo = None
        if "in repository" in text:
            repo = text.split("in repository")[-1].strip()
        if not repo:
            repo = load_current_repo() or input("Repository name: ").strip()
        check_workflow_status(repo)
        return




    # ---- Repository creation ----
    if "create" in text and ("repo" in text or "repository" in text):
        parts = text.split()
        repo = parts[-1]
        create_github_repo(repo)
        return

    # ---- Push ----
    elif "push" in text:
        repo = None
        if "to" in text:
            repo = text.split("to")[-1].strip()
        action_push_folder(repo)
        return
    
    elif "pull" in text:
        repo = None
        if "from" in text:
           repo = text.split("from")[-1].strip()
        if not repo:
           repo = load_current_repo() or input("Repository name: ").strip()
           repo = repo.replace("repository", "").replace("repo", "").strip()
        git_pull(repo)
        return


    # ---- Collaborators ----
    elif "add" in text and ("collaborator" in text or "member" in text):
        collaborator = None
        repo = None
        parts = text.split("collaborator")
        if len(parts) > 1:
            remainder = parts[1].strip()
            tokens = remainder.split()
            if tokens:
                collaborator = tokens[0].replace("@", "").strip(",. ")
        if "to repository" in text:
            repo = text.split("to repository")[-1].strip()
        elif "to" in text:
            repo = text.split("to")[-1].strip()
        if not collaborator:
            speak("Please type collaborator username:")
            collaborator = input("Collaborator username/email: ").strip()
        if not repo:
            repo = load_current_repo() or input("Repository name: ").strip()
        add_collaborator(repo, collaborator)
        return
    
        # ---- Delete Repository ----
    elif "delete" in text and ("repo" in text or "repository" in text):
        repo = None
        if "repository" in text:
            repo = text.split("repository")[-1].strip()
        elif "repo" in text:
            repo = text.split("repo")[-1].strip()
        if not repo:
            repo = load_current_repo() or input("Repository name to delete: ").strip()
        delete_github_repo(repo)
        return
    

    # ---- Fallback ----
    else:
        speak("Sorry, I can create repositories, push folders, manage collaborators, and handle issues.")

if __name__ == "__main__":
    mode = input("🎤 Choose input mode — Voice (v) or Text (t) [auto fallback]: ").strip().lower()

    if mode == "v":
        text = listen_command()
        if text is None:
            print("⚠️ No microphone detected or no speech heard. Switching to text mode...")
            text = input("💬 Type your command: ").strip()
    else:
        text = input("💬 Type your command: ").strip()

    # Call only when we have a real command
    if text:
        parse_and_run_command(text)
    else:
        print("⚠️ No valid input received.")
