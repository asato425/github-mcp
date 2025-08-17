import requests

# MCPサーバのURL
MCP_SERVER_URL = "http://localhost:8000/commit"

def commit_via_mcp(message, repo_path=None):
    payload = {
        "message": message,
        "repo_path": repo_path
    }
    response = requests.post(MCP_SERVER_URL, json=payload)
    if response.ok:
        print("結果:", response.json())
    else:
        print("エラー:", response.text)

if __name__ == "__main__":
    # 標準入力からコミットメッセージを受け取る
    message = input("コミットメッセージを入力してください: ")
    # 必要に応じてパスを指定（例: "." でカレントディレクトリ）
    repo_path = "."
    commit_via_mcp(message, repo_path=repo_path)