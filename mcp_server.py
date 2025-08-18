from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import subprocess
import requests
import os

app = FastAPI(title="GitHub MCP Server")

class CommitRequest(BaseModel):
    message: str
    repo_path: Optional[str] = None  # 省略時はカレントディレクトリを使用

class CommitResponse(BaseModel):
    status: str
    message: str

class PushRequest(BaseModel):
    repo_path: Optional[str] = None  # 省略時はカレントディレクトリを使用

class PushResponse(BaseModel):
    status: str
    message: str
    

class WorkflowRequest(BaseModel):
    owner: str
    repo: str

class WorkflowResult(BaseModel):
    status: str
    conclusion: str
    html_url: str
    logs_url: str

@app.post("/commit", response_model=CommitResponse)
async def commit_code(req: CommitRequest):
    repo_dir = req.repo_path or os.getcwd()
    try:
        # Git コマンドを実行
        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", req.message], cwd=repo_dir, check=True)
        return CommitResponse(status="success", message=f"Committed in {repo_dir}: {req.message}")
    except subprocess.CalledProcessError as e:
        return CommitResponse(status="error", message=str(e))

# push専用エンドポイント
@app.post("/push", response_model=PushResponse)
async def push_code(req: PushRequest):
    repo_dir = req.repo_path or os.getcwd()
    try:
        subprocess.run(["git", "push"], cwd=repo_dir, check=True)
        return PushResponse(status="success", message=f"Pushed in {repo_dir}")
    except subprocess.CalledProcessError as e:
        return PushResponse(status="error", message=str(e))

# export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxをターミナルで実行しておく必要があります
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # セキュリティのため環境変数で

# POSTエンドポイント化し、owner/repoをリクエストボディで受け取る
@app.post("/workflow/latest", response_model=WorkflowResult)
async def get_latest_workflow(req: WorkflowRequest):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{req.owner}/{req.repo}/actions/runs?per_page=1"
    try:
        resp = requests.get(url, headers=headers)
        data = resp.json()
        if "workflow_runs" not in data or not data["workflow_runs"]:
            return WorkflowResult(status="not_found", conclusion="", html_url="", logs_url="")
        run = data["workflow_runs"][0]
        return WorkflowResult(
            status=run["status"],
            conclusion=run["conclusion"],
            html_url=run["html_url"],
            logs_url=run["logs_url"]
        )
    except Exception as e:
        return WorkflowResult(status="error", conclusion=str(e), html_url="", logs_url="")