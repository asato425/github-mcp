from mcp_client import get_workflow_result_from_commit
import time
if __name__ == "__main__":
    # 標準入力からコミットメッセージを受け取る
    #message = input("コミットメッセージを入力してください: ")
    # メッセージには今の時刻を入れたい
    commit_message = f"コミット時刻: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    # 必要に応じてパスを指定（例: "." でカレントディレクトリ）
    owner = "asato425"
    github_repo = "github-mcp"
    get_workflow_result_from_commit(owner, github_repo, commit_message)