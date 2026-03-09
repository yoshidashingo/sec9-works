# /sync-meetings - ミーティング議事録・書き起こし自動同期

ミーティング議事録をcircleback MCPサーバーから取得し、mdファイルとして同期する。

## 引数の解釈

`$ARGUMENTS` を解析する:

- 引数なし → Sec9（circleback）を同期
- `--since YYYY-MM-DD` → 指定日以降のミーティングのみ取得

---

## Sec9同期手順（circleback）

### ステップ1: 同期状態の読み込み

`meetings/_sync-state.json` を Read ツールで読み込む。

- ファイルが存在しない場合、以下のデフォルト値で初期化する:
  ```json
  {
    "last_sync": "<30日前のISO 8601日時>",
    "synced_meeting_ids": [],
    "provider": "circleback"
  }
  ```
- `--since` が指定されている場合、`last_sync` をその日付に上書きする。

### ステップ2: ミーティング一覧の取得

ToolSearch で `circleback` を検索してツールをロードし、以下を実行:

```
mcp__circleback__SearchMeetings を呼び出す
パラメータ: startDate = last_sync の日付(YYYY-MM-DD), pageIndex = 0
```

- 1ページあたり最大20件。結果が20件の場合、次のページ（pageIndex + 1）も取得する。全ページ取得するまでループ。
- `synced_meeting_ids` に含まれるミーティングはスキップする。

### ステップ3: 各ミーティングの詳細取得とmd生成

未同期のミーティングごとに以下を実行:

1. **ノート・アクションアイテム取得**: `mcp__circleback__ReadMeetings` でミーティングのノート、アクションアイテム、AIインサイトを取得（ミーティングIDの配列を渡す）
2. **トランスクリプト取得**: `mcp__circleback__GetTranscriptsForMeetings` で書き起こし全文を取得（最大50件/バッチ）

取得した情報を以下のテンプレートに従ってmdファイルを生成し、`meetings/` に書き出す。

#### ファイル命名規則

```
{YYYY-MM-DD}_{sanitized-meeting-name}.md
```

- ミーティング名をサニタイズ: 英数字・ハイフン・アンダースコアのみ残す、スペースはハイフンに、日本語はローマ字化せずそのまま除去、80文字で切り詰め、すべて小文字
- 同名・同日のファイルが既に存在する場合は末尾に `_2`, `_3` を付与

#### mdテンプレート（Sec9/circleback）

```markdown
# {meeting_name}

- **日時**: {date} {start_time} - {end_time}
- **参加者**: {participants をカンマ区切りで列挙}
- **時間**: {duration}
- **ソース**: circleback
- **Meeting ID**: {meeting_id}

---

## ノート・ハイライト

{notes / AI insights の内容をそのまま記載。なければ「ノートはありません」}

## アクションアイテム

{action items を箇条書きで記載。なければ「アクションアイテムはありません」}

---

## トランスクリプト

{タイムスタンプ付きの書き起こし全文。話者名を含む。なければ「トランスクリプトはありません」}
```

### ステップ4: 同期状態の更新

すべてのミーティングの処理が完了したら、`meetings/_sync-state.json` を更新:

```json
{
  "last_sync": "<現在のISO 8601日時>",
  "synced_meeting_ids": ["既存のID", "新しく同期したID"],
  "provider": "circleback"
}
```

Write ツールでファイルを書き出す。

---

## 実行後の出力

同期完了後、以下のサマリーを表示する:

```
## 同期結果

### Sec9 (circleback)
- 新規同期: {件数}件
- スキップ（同期済み）: {件数}件
- 保存先: meetings/
```

## エラーハンドリング

- MCPツールの呼び出しに失敗した場合、エラー内容を表示して該当ミーティングをスキップし、次のミーティングの処理を続行する。
- スキップしたミーティングは `synced_meeting_ids` に追加しない（次回の同期で再試行される）。
- 全件失敗した場合でも `_sync-state.json` の `last_sync` は更新しない。
