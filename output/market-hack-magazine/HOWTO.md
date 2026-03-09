# Market Hack Magazine 記事収集 HOWTO

## 概要

広瀬隆雄氏のnote定期購読マガジン「Market Hack Magazine」の記事本文を、Gmailの通知メールから収集し `references/market-hack-magazine-articles.md` に蓄積する手順。

## 前提条件

- Sec9社のGoogleアカウント（admin@sec9.co.jp）でnoteの定期購読中
- MCPサーバー `google-workspace-sec9` が利用可能
- Gmail APIが有効化済み（プロジェクトID: 220197655643）

## 収集手順

### 1. Gmailから Market Hack Magazine の記事メールを検索

```
ツール: mcp__google-workspace-sec9__search_gmail_messages
パラメータ:
  query: "note market hack"
  user_google_email: "admin@sec9.co.jp"
  page_size: 10
```

- 検索結果にはページネーションがある。`page_token` を使って全ページ取得する
- 1ページあたり最大10件

### 2. メール本文をバッチ取得

```
ツール: mcp__google-workspace-sec9__get_gmail_messages_content_batch
パラメータ:
  message_ids: [検索結果のMessage IDリスト]
  user_google_email: "admin@sec9.co.jp"
  format: "full"
```

- 1回のバッチで最大25件まで取得可能
- Subject が「Market Hack Magazine更新のおしらせ」のメールのみが対象
- noteからの他のマガジン通知（黒塗りなしパッケージ等）や購入確認メールは除外する

### 3. 記事のフィルタリング

以下の条件で Market Hack Magazine の記事のみを抽出する:

- **採用**: Subject が「Market Hack Magazine更新のおしらせ」
- **除外**: 定期購読完了通知、購入完了通知、他マガジンの更新通知、無関係なメール

### 4. references への書き込み

`references/market-hack-magazine-articles.md` に追記する。

記事フォーマット:

```markdown
## YYYY-MM-DD: 記事タイトル

記事本文（noteメール通知のフッター「スキする」以降は除外）
```

- 日付降順（新しい記事が上）で記載
- ヘッダーの記事数と期間を更新する
- メール本文からnote固有のフッター（「スキする」「スキとは?」「ヘルプ / プライバシーポリシー / 利用規約」）は除外する

## 定期更新の手順

### 差分更新の方法

1. `references/market-hack-magazine-articles.md` の最新記事の日付を確認する
2. Gmail検索で、その日付以降の記事のみを取得する:
   ```
   query: "note market hack after:YYYY/MM/DD"
   ```
3. 既存ファイルの先頭（ヘッダー直後）に新しい記事を追記する
4. ヘッダーの記事数と期間を更新する

### 更新頻度の目安

- 広瀬氏は概ね毎日1〜3本の記事を投稿している
- 週1回程度の更新で十分

## 注意事項

- これはSec9社のクライアントワークなので、MCPサーバーは `google-workspace-sec9` を使用すること（`google-workspace-ga` ではない）
- メールの送信元は `noreply@note.com`（旧: `noreply@note.mu`）
- 記事本文はメール通知に全文含まれているため、noteサイトへのアクセスは不要
