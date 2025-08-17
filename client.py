import requests


# MCPサーバのURL
MCP_COMMIT_URL = "http://localhost:8000/commit"
MCP_PUSH_URL = "http://localhost:8000/push"


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


# プッシュ用の関数を追加してほしい

if __name__ == "__main__":
    # 標準入力からコミットメッセージを受け取る
    message = input("コミットメッセージを入力してください: ")
    # 必要に応じてパスを指定（例: "." でカレントディレクトリ）
    repo_path = "."
    commit_via_mcp(message, repo_path=repo_path)
    # pushも実行
    push_via_mcp(repo_path=repo_path)