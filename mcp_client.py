import requests
import time


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

def wait_for_latest_workflow_result(owner, repo, interval=5, timeout=300):
    """
    最新ワークフローが完了するまで待機し、完了後にその結果を返す
    :param owner: GitHubユーザー名または組織名
    :param repo: リポジトリ名
    :param interval: ポーリング間隔（秒）
    :param timeout: 最大待機時間（秒）
    :return: 完了したワークフローの情報
    """
    start = time.time()
    MCP_WORKFLOW_URL = "http://localhost:8000/workflow/latest"
    payload = {"owner": owner, "repo": repo}
    while True:
        response = requests.post(MCP_WORKFLOW_URL, json=payload)
        if not response.ok:
            print("ワークフローエラー:", response.text)
            return None
        data = response.json()
        status = data.get("status")
        if status not in ("in_progress", "queued"):
            print("ワークフロー完了:", data)
            return data
        if time.time() - start > timeout:
            print("タイムアウトしました")
            return None
        print(f"ワークフロー実行中（status={status}）...待機中")
        time.sleep(interval)

