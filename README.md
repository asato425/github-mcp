# github-mcp
研究用のGitHub MCPサーバーの実装をする

```bash
# インストールしたパッケージをrequirements.txtに記載
$ pip freeze > requirements.txt

# requirements.txtに記載されたパッケージをインストール
$ pip install -r requirements.txt

# サーバーの実行方法,http://localhost:8000/docs にアクセスするとAPIの動作確認もできる
$ uvicorn mcp_server:app --reload
```