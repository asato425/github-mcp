# github-mcp
研究用のGitHub MCPサーバーの実装をする

```bash
# 仮想環境の作成
$ python3 -m venv .venv

# 仮想環境の有効化
$ source .venv/bin/activate

# requirements.txtに記載されたパッケージをインストール
$ pip install -r requirements.txt

# インストールしたパッケージをrequirements.txtに記載
$ pip freeze > requirements.txt

# GitHubトークンの登録
$ export GITHUB_TOKEN=*********

# サーバーの実行方法,http://localhost:8000/docs にアクセスするとAPIの動作確認もできる
$ uvicorn mcp_server:app --reload
```