# 🤖 AI Code Reviewer

An autonomous GitHub Pull Request reviewer powered by LLMs. When a PR is opened, this tool automatically analyzes the code changes and posts a detailed review comment — catching bugs, security vulnerabilities, and bad practices in seconds.

## 🎬 Demo

> Open a Pull Request → Get an instant AI review posted as a comment

![AI Code Reviewer Demo](https://raw.githubusercontent.com/Utkarsh182003/AI-Code/main/demo.png)

---

## 🧠 How It Works

1. Developer opens a Pull Request on GitHub
2. GitHub sends a webhook event to the FastAPI server
3. Server verifies the request signature (security)
4. Changed files and diffs are fetched via GitHub API
5. Code is sent to Groq (Llama 3.3 70B) for analysis
6. A structured review is automatically posted as a PR comment

---

## 🏗️ Architecture

GitHub PR opened
│
▼
GitHub Webhook (POST /webhook)
│
▼
FastAPI Server (main.py)
│
├── Signature Verification (HMAC SHA256)
│
├── PR Diff Fetcher (github_client.py)
│         │
│         └── PyGithub → Fetch changed files + patches
│
├── AI Reviewer (reviewer.py)
│         │
│         └── Groq API (Llama 3.3 70B) → Analyze code
│
└── Comment Poster (github_client.py)
│
└── Post structured review to PR

---

## 🔍 What It Detects

- 🐛 **Bugs** — division by zero, infinite recursion, unhandled exceptions
- 🔒 **Security Issues** — SQL injection, hardcoded secrets, command injection, eval() usage
- 📦 **Bad Practices** — pickle deserialization, plain text passwords, unvalidated inputs
- 💡 **Improvements** — code quality, performance, readability suggestions
- ✅ **Verdict** — APPROVE / REQUEST CHANGES / NEEDS DISCUSSION

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| LLM | Groq API (Llama 3.3 70B) |
| GitHub Integration | PyGithub + Webhooks |
| Security | HMAC SHA256 signature verification |
| Config | Python dotenv |

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Utkarsh182003/ai-code-reviewer
cd ai-code-reviewer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Fill in your keys in `.env`:
GROQ_API_KEY=your_groq_api_key
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_TOKEN=your_github_token

### 5. Start the server
```bash
uvicorn main:app --reload --port 8000
```

### 6. Expose locally with ngrok
```bash
ngrok http 8000
```

### 7. Add webhook to your GitHub repo
- Go to repo Settings → Webhooks → Add webhook
- Payload URL: `https://your-ngrok-url/webhook`
- Content type: `application/json`
- Secret: your webhook secret
- Events: Pull requests only

---

## 📁 Project Structure
ai-code-reviewer/
├── main.py              # FastAPI app entry point
├── webhook.py           # GitHub webhook handler
├── github_client.py     # GitHub API — fetch diffs, post comments
├── reviewer.py          # Groq LLM code review logic
├── requirements.txt     # Dependencies
├── .env.example         # Environment variable template
└── README.md            # You are here

---

## 🔐 Security

- Webhook payloads are verified using **HMAC SHA256** signatures
- All secrets stored in environment variables, never hardcoded
- Non-code files (images, PDFs, lock files) are automatically skipped

---

## 📌 Future Improvements

- [ ] Line-by-line inline comments on the PR diff
- [ ] Support for multiple LLM backends (OpenAI, Gemini)
- [ ] Severity scoring for issues found
- [ ] Deploy on Railway/Render for always-on reviewing
- [ ] Fine-tune model on company-specific coding standards

---

## 👤 Author

**Utkarsh Pathak**
[LinkedIn](https://www.linkedin.com/in/utkarshpathak18) • [GitHub](https://github.com/Utkarsh182003)