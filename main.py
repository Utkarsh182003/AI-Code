from fastapi import FastAPI
from webhook import router as webhook_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Code Reviewer",
    description="Automatically reviews GitHub PRs using AI",
    version="1.0.0"
)

app.include_router(webhook_router)

@app.get("/")
def health_check():
    return {"status": "AI Code Reviewer is running"}