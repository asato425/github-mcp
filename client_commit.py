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
    # 例: カレントディレクトリでコミット
    commit_via_mcp("テストコミット", repo_path=".")