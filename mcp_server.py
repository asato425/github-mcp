# mcp_commit_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import subprocess
import os

app = FastAPI(title="Git Commit MCP Server")

class CommitRequest(BaseModel):
    message: str
    repo_path: Optional[str] = None  # 省略時はカレントディレクトリを使用

class CommitResponse(BaseModel):
    status: str
    message: str

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
