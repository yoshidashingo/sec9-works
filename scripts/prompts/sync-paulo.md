# パウロ メンバーシップ記事同期

Gmailからパウロ氏のnoteメンバーシップ記事を取得し、`output/paulo-newsletter/references/paulo-newsletter-articles.md` に差分追記する。

## ステップ1: 同期状態の読み込み

`output/paulo-newsletter/references/_sync-state.json` を Read で読み込む。

- ファイルが存在しない場合:
  ```json
  {"last_sync_date": "2026/01/01", "synced_message_ids": [], "provider": "gmail-sec9"}
  ```

## ステップ2: Gmailから記事メールを検索

ToolSearch で `google-workspace-sec9` の Gmail ツールを検索してロードし、`mcp__google-workspace-sec9__search_gmail_messages` を呼び出す。

```
query: "from:noreply@note.com パウロ after:{last_sync_date の値をそのまま埋め込む}"
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

- **採用**: From ヘッダーの表示名が「パウロ」を含むメールのみ（例: `"パウロ" <noreply@note.com>`）
- **除外**: From 表示名が「パウロ」を含まないnoteメール、購入確認通知、定期購読通知

## ステップ5: 既存ファイルへの差分挿入

`output/paulo-newsletter/references/paulo-newsletter-articles.md` の先頭20行のみを Read で読み込む（ヘッダー確認用。ファイル全体は読まない）。

新しい記事ごとに:

1. Subject が記事タイトル。Date ヘッダーから YYYY-MM-DD を抽出
2. 本文からnoteフッターを除去。除去開始位置: 「スキする」の最初の出現箇所
3. 本文冒頭の重複パターンを除去。noteメールは冒頭に `{タイトル} サイトで確認する{タイトル}` という重複がある。例: `K型半導体市場の幕開け サイトで確認するK型半導体市場の幕開け 1. TSMC...` → `1. TSMC...` から採用する。具体的には「サイトで確認する」の後のタイトル末尾の次の文字から本文開始とする

**Edit ツール**で差分挿入する（Write でファイル全体を書き出さないこと）:

```
file_path: "output/paulo-newsletter/references/paulo-newsletter-articles.md"
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
