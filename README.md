advasa-test-1
================

Docker Compose で Django を起動するための最小雛形です。実装（モデル/シリアライザ/ビュー/テンプレート/JWT/管理コマンド/テスト）は候補者の課題として未実装です。

含まれるもの
- Django 4.2 / PostgreSQL / docker-compose 一式
- ライブラリは DRF と SimpleJWT を requirements に含め済み（設定は未適用）

前提
- Docker / Docker Compose がインストール済み

Docker/Compose のインストール
- macOS (Docker Desktop 推奨)
  - `brew install --cask docker`
  - アプリケーションから Docker を起動（初回は権限付与が必要）
  - 確認: `docker --version && docker compose version`
- Ubuntu/Debian（公式レポジトリ）
  - `sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg`
  - `sudo install -m 0755 -d /etc/apt/keyrings`
  - `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`
  - `echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
  - `sudo apt-get update`
  - `sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`
  - （任意）非rootで実行: `sudo usermod -aG docker $USER` → 一度ログアウト/ログイン
  - 確認: `docker --version && docker compose version`
- Windows: Docker Desktop（https://www.docker.com/products/docker-desktop/）をインストールし、同様にバージョン確認

起動手順
1. `.env` を作成（`.env.example` をコピー）
2. `docker compose up -d --build`
3. ブラウザで http://localhost:8000/ にアクセス（初期状態は管理サイトのみ）

環境変数（.env）
- `DJANGO_SECRET_KEY`（任意）
- `DEBUG=true`
- `DB_NAME=advasa`
- `DB_USER=advasa`
- `DB_PASSWORD=advasa`
- `DB_HOST=db`
- `DB_PORT=5432`

次のステップ
- 実装課題は `TASKS.md` を参照してください。
