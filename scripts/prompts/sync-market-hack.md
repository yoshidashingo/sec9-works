# Market Hack Magazine 記事同期

Gmailから広瀬隆雄氏のnote記事を取得し、`output/market-hack-magazine/references/market-hack-magazine-articles.md` に差分追記する。

## ステップ1: 同期状態の読み込み

`output/market-hack-magazine/references/_sync-state.json` を Read で読み込む。

- ファイルが存在しない場合:
  ```json
  {"last_sync_date": "2026/02/19", "synced_message_ids": [], "provider": "gmail-sec9"}
  ```

## ステップ2: Gmailから記事メールを検索

ToolSearch で `google-workspace-sec9` の Gmail ツールを検索してロードし、`mcp__google-workspace-sec9__search_gmail_messages` を呼び出す。

```
query: "from:noreply@note.com subject:Market Hack Magazine更新のおしらせ after:{last_sync_date の値をそのまま埋め込む}"
user_google_email: "admin@sec9.co.jp"
page_size: 25
```

- `page_token` がある場合は最大5ページまで取得する。
- 結果が0件なら「新規記事なし」として終了。

## ステップ3: メール本文をバッチ取得

`mcp__google-workspace-sec9__get_gmail_messages_content_batch` で本文を取得。

```
message_ids: [検索結果のMessage IDリスト（synced_message_idsに含まれるIDは除外）]
user_google_email: "admin@sec9.co.jp"
format: "full"
```

- 最大25件/バッチ。超える場合は分割。
- synced_message_ids に含まれるIDはバッチ取得自体をスキップする。

## ステップ4: フィルタリング

- **採用**: Subject に「Market Hack Magazine更新のおしらせ」を含むメールのみ
- **除外**: 定期購読完了通知、購入完了通知、他マガジン更新通知

## ステップ5: 既存ファイルへの差分挿入

`output/market-hack-magazine/references/market-hack-magazine-articles.md` の先頭20行のみを Read で読み込む（ヘッダー確認用。ファイル全体は読まない）。

新しい記事ごとに:

1. 記事タイトルは本文の冒頭行から抽出する（Subject は固定文言のため使わない）。日付はメールの Date ヘッダーから YYYY-MM-DD で取得
2. 本文からnoteフッターを除去。除去開始位置: 「スキする」の最初の出現箇所
3. 既に synced_message_ids に含まれるメールはスキップ済みのため、追加の重複チェックは不要

**Edit ツール**で差分挿入する（Write でファイル全体を書き出さないこと）:

```
file_path: "output/market-hack-magazine/references/market-hack-magazine-articles.md"
old_string: ヘッダー末尾の最初の "---" の行（改行含む）
new_string: "---" + 新記事ブロック（日付降順）
```

記事ブロックのフォーマット:
```markdown
---

## YYYY-MM-DD: 記事タイトル

記事本文

```

複数記事がある場合は日付降順にソートし、1回の Edit で全記事を挿入する。

最後にヘッダーの「収集日」「記事数」「期間」を Edit で更新する。記事数は既存ヘッダーの数値 + 新規記事数で計算する。

## ステップ6: 同期状態の更新

Write で `_sync-state.json` を更新。synced_message_ids には既存IDと新規IDを統合する。

```json
{
  "last_sync_date": "<最新記事の日付 YYYY/MM/DD>",
  "synced_message_ids": ["既存ID", "新規Message ID"],
  "provider": "gmail-sec9"
}
```

**注意**: last_sync_date は処理した記事の日付を使う。本日より未来の日付を設定してはならない。

## エラー時

Gmail API失敗時はエラーを出力して終了。既存ファイルへの Edit は行わない。
全てのメール取得が完了してからステップ5の Edit を実行すること。
