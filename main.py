from mcp_client import commit_via_mcp, push_via_mcp, get_latest_workflow_logs, wait_for_latest_workflow_result

if __name__ == "__main__":
    # 標準入力からコミットメッセージを受け取る
    #message = input("コミットメッセージを入力してください: ")
    message = "最新のワークフロー結果を取得できるかテスト"
    # 必要に応じてパスを指定（例: "." でカレントディレクトリ）
    repo_path = "."
    commit_via_mcp(message, repo_path=repo_path)
    # pushも実行
    push_via_mcp(repo_path=repo_path)
    owner = "asato425"
    github_repo = "github-mcp"
    wait_for_latest_workflow_result(owner, github_repo)