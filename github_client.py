from github import Github
import os

def get_github_client():
    token = os.getenv("GITHUB_TOKEN")
    return Github(token)

def get_pr_diff(repo_full_name: str, pr_number: int) -> list[dict]:
    """
    Fetches all changed files and their diffs from a pull request
    Returns a list of dicts with filename, status and the actual code changes
    """
    g = get_github_client()
    repo = g.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)

    files_data = []

    for file in pr.get_files():
        # Skip files that are too large or binary files
        if file.patch is None:
            print(f"Skipping {file.filename} - no patch available")
            continue

        # Skip non-code files
        skip_extensions = [
            '.png', '.jpg', '.jpeg', '.gif', '.svg',
            '.ico', '.pdf', '.zip', '.lock'
        ]
        if any(file.filename.endswith(ext) for ext in skip_extensions):
            print(f"Skipping {file.filename} - non-code file")
            continue

        files_data.append({
            "filename": file.filename,
            "status": file.status,        # added, modified, removed
            "additions": file.additions,
            "deletions": file.deletions,
            "patch": file.patch           # actual code diff
        })

    print(f"Fetched {len(files_data)} code files from PR #{pr_number}")
    return files_data


def post_pr_comment(repo_full_name: str, pr_number: int, comment: str):
    """
    Posts the AI review as a comment on the pull request
    """
    g = get_github_client()
    repo = g.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment)
    print(f"Posted review comment on PR #{pr_number}")