候補者向け実装課題（8〜10時間想定）
=================================

目的
- Django + DRF + SimpleJWT を用いた簡易申請アプリのサーバー実装
- 申請金額は「整数のみ」を扱う
- Docker Compose で環境は起動済み（Django/DB のみ稼働）。以降の実装を行ってください。

使用技術（すでに requirements に含有）
- Django 4.2 / Django REST Framework / djangorestframework-simplejwt
- DB: PostgreSQL（compose で起動）

開発ルール
- アプリ名は `core`
- 金額は 1 以上の整数のみ（小数不可）
- バリデーションはサーバー側で必須（クライアント側は任意）
- 認証は JWT（SimpleJWT）
- テンプレートは Django テンプレート（Next.js などは不要）

優先度ガイド
- 高: JWT 発行/更新（/api/auth/*）、申請作成 API（POST /api/applications/）
- 中: `/api/me`、申請一覧（GET /api/applications/）、テンプレートの最小実装
- 低: 単体テスト、管理コマンド（add_allowance）

提出物
- 実装コード一式（`core/` 配下、テンプレート、設定変更）
- 最低限の単体テスト（後述の観点）
- 簡単な動作手順（README 追記またはメモ）
- 全てのタスクが完了していなくても構いません
- 実装した機能と未実装の機能を README に明記してください
- 時間配分と優先順位の判断理由を簡潔に説明してください

実装タスク（MUST）
1) アプリ作成と設定
- `python manage.py startapp core`
- `settings.py` の `INSTALLED_APPS` に `core` を追加
- `urls.py` に後述のエンドポイントを配線
  - テンプレートディレクトリは `templates/` を利用（既存フォルダあり）

2) モデル
- `UserProfile`: `user(OneToOne, AUTH_USER)` / `available_amount(IntegerField, default=0)`
- `Application`: `user(FK)` / `amount(IntegerField)` / `status(CharField, default='SUBMITTED')` / `created_at(DateTime, auto_now_add=True)`
- ユーザー作成時に `UserProfile` を自動生成するシグナルを追加
- マイグレーション作成・適用
 - 任意（推奨）: `Application(user, -created_at)` のインデックスを追加

3) 認証（JWT）
- SimpleJWT を導入し、以下を有効化
  - `POST /api/auth/token/`（username/password -> access/refresh）
  - `POST /api/auth/token/refresh/`
- DRF のデフォルト認証を JWT（`REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES`）に設定
- 既定パーミッションは `AllowAny`、各Viewで必要に応じて上書き
- 初回ログイン用ユーザーは `docker compose exec web python manage.py createsuperuser` で作成して構いません（その認証情報でトークン取得可能）
- ユーザー作成は以下のいずれでも可:
  - DRFのブラウザAPI（実装後の `POST /api/users/`）
  - `shell_plus` での作成

4) API
- `GET /api/me/`（JWT必須）
  - レスポンス: `{ id, username, available_amount }`
- `POST /api/users/`（ユーザー作成）
  - 入力: `{ username, password, initial_allowance? }`
  - `initial_allowance` があれば `available_amount` に反映
- `GET /api/applications/`（本人のみ）
  - ページネーション（PageNumberPagination, page_size=10）
  - 並びは新しい順
- `POST /api/applications/`
  - 入力: `{ amount: int }`（1 以上の整数）
  - トランザクション内で `UserProfile` を `select_for_update` し、`available_amount` を減算
  - 残高不足は 400 を返却: `{ "amount": ["申請可能額を超えています"] }`

API仕様（例）
- 取得トークン: `POST /api/auth/token/`
  - 入力: `{ "username": "alice", "password": "pass" }`
  - 出力: `{ "access": "...", "refresh": "..." }`
- 自分情報: `GET /api/me/` → `{ "id": 1, "username": "alice", "available_amount": 5000 }`
- 申請作成: `POST /api/applications/`
  - 入力: `{ "amount": 1000 }`
  - 出力: `{ "id": 3, "amount": 1000, "status": "SUBMITTED", "created_at": "2025-01-01T00:00:00Z" }`
- エラー形式
  - バリデーション（400）: `{ "field": ["メッセージ"] }`
  - 未認証（401）、権限不正（403）、未発見（404）

5) テンプレート（ページ）
- `/login/`:
  - username/password で JWT を取得し `localStorage` に保存
  - 成功で `/apply/` へ
- `/apply/`:
  - `GET /api/me/` で現在の申請可能額を表示
  - 金額（整数）の入力フォームと申請ボタン
  - 成功で `/complete/` へ（直前の金額/日時を表示できれば尚可）
- `/complete/`:
  - 申請完了の表示、`申請画面に戻る` リンク
- `/history/`:
  - `GET /api/applications/` の結果をテーブル表示（簡易で可）
 - 備考: API呼び出し時は `Authorization: Bearer <access>` ヘッダを付与

6) 管理コマンド
- `python manage.py add_allowance --amount 100`:
  - 全ユーザーの `available_amount` を整数で加算
- `amount` は 1 以上の整数のみ

データ操作の補助（shell_plus 利用可）
- 目的: 開発中の動作確認として `available_amount` の調整やユーザー作成を手早く実施
- 起動（docker compose 経由）:
  - `docker compose exec web python manage.py shell_plus`
- 例: ユーザー作成と残高変更（`core` 実装後に利用可）
  ```python
  from django.contrib.auth import get_user_model
  from core.models import UserProfile
  User = get_user_model()
  u, _ = User.objects.get_or_create(username='alice')
  u.set_password('password'); u.save()
  # プロファイル（シグナルで自動作成される想定）
  u.profile.available_amount = 5000
  u.profile.save(update_fields=['available_amount'])
  ```

7) 単体テスト
- 例（pytest ではなく Django TestCase でOK）
  - `/api/me/` が `available_amount` を返す
  - 申請成功で `available_amount` が減算される
  - 残高不足の申請が 400 になる
  - 管理コマンドで加算される

推奨実装順序
1. アプリ作成・設定・URL枠
2. モデル/マイグレーション/シグナル
3. JWT導入・`/api/auth/*`・`/api/me`
4. 申請API（POST/GET, 残高更新, ページネーション）
5. テンプレ（login/apply/complete/history）
6. 管理コマンド
7. 単体テスト・微修正

受け入れ基準
- ログイン→申請→完了→履歴の一連の操作がテンプレートで可能
- サーバー側で金額が整数のみ許容されること（0 以下や小数はエラー）
- 残高不足時に 400 と適切なエラーメッセージ
- `add_allowance` コマンドにより全ユーザーの残高が加算される
- 上記に対する最小限の単体テストが通る

動作確認コマンド例
- `docker compose up -d --build`
- `docker compose exec web python manage.py migrate`
- 最初のユーザー作成: `docker compose exec web python manage.py createsuperuser`
- テスト: `docker compose exec web python manage.py test`
 - 開発用シェル: `docker compose exec web python manage.py shell_plus`

補足
- フロントは Django テンプレートのみでOK（Next.js不要）
- CSRF と JWT は混同しない（API は `Authorization: Bearer <access>`）
- 余裕があれば Admin の最低限の調整（任意）
 - タイムゾーン: UTC（表示は任意）。言語: ja
 - コードスタイル: PEP8 準拠、型ヒントは任意だが推奨
 - コミットは機能単位で細かく分割（任意）
