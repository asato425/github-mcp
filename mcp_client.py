import requests


# MCPサーバのURL
MCP_COMMIT_URL = "http://localhost:8000/commit"
MCP_PUSH_URL = "http://localhost:8000/push"
MCP_WORKFLOW_URL = "http://localhost:8000/workflow/latest"


def commit_via_mcp(message, repo_path=None):
    payload = {
        "message": message,
        "repo_path": repo_path
    }
    response = requests.post(MCP_COMMIT_URL, json=payload)
    if response.ok:
        print("コミット結果:", response.json())
    else:
        print("コミットエラー:", response.text)

def push_via_mcp(repo_path=None):
    payload = {
        "repo_path": repo_path
    }
    response = requests.post(MCP_PUSH_URL, json=payload)
    if response.ok:
        print("プッシュ結果:", response.json())
    else:
        print("プッシュエラー:", response.text)

def get_latest_workflow_logs(owner, repo):
    payload = {
        "owner": owner,
        "repo": repo
    }
    response = requests.post(MCP_WORKFLOW_URL, json=payload)
    if response.ok:
        print("ワークフロー結果:", response.json())
    else:
        print("ワークフローエラー:", response.text)
