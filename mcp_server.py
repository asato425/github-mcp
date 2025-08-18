from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import subprocess
import requests
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
app = FastAPI(title="GitHub MCP Server")

class CommitRequest(BaseModel):
    message: str
    repo_path: Optional[str] = None  # 省略時はカレントディレクトリを使用

class CommitResponse(BaseModel):
    status: str
    message: str
    commit_sha: str

class PushRequest(BaseModel):
    repo_path: Optional[str] = None  # 省略時はカレントディレクトリを使用

class PushResponse(BaseModel):
    status: str
    message: str
    

class WorkflowRequest(BaseModel):
    owner: str
    repo: str
    commit_sha: str

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
        commit_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, check=True, capture_output=True).stdout.decode().strip()
        return CommitResponse(status="success", message=f"Committed in {repo_dir}: {req.message}", commit_sha=commit_sha)
    except subprocess.CalledProcessError as e:
        return CommitResponse(status="error", message=str(e), commit_sha=commit_sha)

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
        poll_count = 0
        found = False
        run = None
        # 最大60回(=最大5分)までポーリング
        while poll_count < 60:
            resp = requests.get(url, headers=headers)
            data = resp.json()
            logging.info("------------------------------------------")
            logging.info({"poll_count": poll_count})
            if "workflow_runs" not in data or not data["workflow_runs"]:
                time.sleep(5)
                poll_count += 1
                continue
            # head_shaが一致するrunを探す
            for r in data["workflow_runs"]:
                if r.get("head_sha") == req.commit_sha:
                    run = r
                    found = True
                    break
            if found:
                # 進行中なら完了まで待機
                while run["status"] in ("in_progress", "queued") and poll_count < 60:
                    time.sleep(5)
                    resp = requests.get(url, headers=headers)
                    data = resp.json()
                    # head_shaが一致するrunを再取得
                    run = None
                    for r in data["workflow_runs"]:
                        if r.get("head_sha") == req.commit_sha:
                            run = r
                            break
                    if run is None:
                        break
                    poll_count += 1
                break
            else:
                # head_sha一致するrunがまだ出てこない場合は少し待つ
                time.sleep(5)
                poll_count += 1
        if not run:
            return WorkflowResult(status="not_found", conclusion="", html_url="", logs_url="")
        logging.info("------------------------------------------")
        logging.info("run: %s", run)
        return WorkflowResult(
            status=run["status"],
            conclusion=run["conclusion"],
            html_url=run["html_url"],
            logs_url=run["logs_url"]
        )
    except Exception as e:
        return WorkflowResult(status="error", conclusion=str(e), html_url="", logs_url="")