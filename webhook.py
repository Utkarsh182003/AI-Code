from fastapi import APIRouter, Request, HTTPException, Header
import hmac
import hashlib
import os
import json
from github_client import get_pr_diff, post_pr_comment
from reviewer import review_code

router = APIRouter()

def verify_signature(payload: bytes, signature: str) -> bool:
    if not signature:
        return False
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "").encode()
    expected = "sha256=" + hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

@router.post("/webhook")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):
    payload_bytes = await request.body()

    if not verify_signature(payload_bytes, x_hub_signature_256 or ""):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(payload_bytes)

    if x_github_event != "pull_request":
        return {"message": f"Ignoring event: {x_github_event}"}

    action = payload.get("action")
    if action not in ["opened", "synchronize"]:
        return {"message": f"Ignoring PR action: {action}"}

    pr_number = payload["pull_request"]["number"]
    repo_full_name = payload["repository"]["full_name"]
    pr_title = payload["pull_request"]["title"]

    print(f"New PR detected: #{pr_number} - {pr_title} in {repo_full_name}")

    # Fetch code changes
    files = get_pr_diff(repo_full_name, pr_number)
    print(f"Fetched {len(files)} files from PR #{pr_number}")

    # Get AI review from Gemini
    review = review_code(files)
    print("Review generated, posting to GitHub...")

    # Post review back to the PR
    post_pr_comment(repo_full_name, pr_number, review)
    print(f"Review posted on PR #{pr_number} successfully!")

    return {
        "message": "PR reviewed successfully",
        "pr_number": pr_number,
        "files_reviewed": len(files)
    }