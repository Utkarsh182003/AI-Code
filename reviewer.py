from groq import Groq
import os

def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(files: list[dict]) -> str:
    prompt = """You are a senior software engineer doing a thorough code review.
Analyze the following code changes from a pull request and provide a detailed review.

Your review must include these sections:

## 📋 Summary
Brief overview of what this PR does.

## 🐛 Bugs & Issues
List any bugs, logic errors, or broken code you find.
If none, write "No bugs found."

## ⚠️ Security Issues
List any security vulnerabilities like SQL injection, exposed secrets, unvalidated inputs etc.
If none, write "No security issues found."

## 💡 Suggestions & Improvements
List improvements for code quality, performance, or best practices.

## ✅ Verdict
One of: APPROVE / REQUEST CHANGES / NEEDS DISCUSSION
And one line explaining why.

---
Here are the changed files:

"""
    for file in files:
        prompt += f"\n### File: `{file['filename']}` ({file['status']})\n"
        prompt += f"Additions: {file['additions']} | Deletions: {file['deletions']}\n"
        prompt += f"```diff\n{file['patch']}\n```\n"

    return prompt


def review_code(files: list[dict]) -> str:
    if not files:
        return "No reviewable code files found in this PR."

    prompt = build_prompt(files)

    print("Sending code to Groq for review...")

    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a senior software engineer who does thorough, helpful code reviews."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=2048,
    )

    print("Review received!")
    return response.choices[0].message.content