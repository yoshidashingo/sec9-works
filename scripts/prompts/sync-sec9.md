# Sec9 ミーティング議事録同期（circleback）

Sec9社のミーティング議事録を circleback から取得し、mdファイルとして `meetings/` に書き出す。

## ステップ1: 同期状態の読み込み

`meetings/_sync-state.json` を Read で読み込む。

- ファイルが存在しない場合:
  ```json
  {
    "last_sync": "<30日前のISO 8601日時>",
    "synced_meeting_ids": [],
    "provider": "circleback"
  }
  ```

## ステップ2: ミーティング一覧の取得

ToolSearch で `circleback` を検索してツールをロードし、`mcp__circleback__SearchMeetings` を呼び出す（startDate = last_sync の日付 YYYY-MM-DD, pageIndex = 0）。

- 結果が20件の場合、次ページ（pageIndex + 1）も取得。全ページ取得するまでループ。
- `synced_meeting_ids` に含まれるミーティングはスキップする。
- 未同期が15件を超える場合は15件のみ処理し、残りは次回に回す。

## ステップ3: 各ミーティングの詳細取得とmd生成

Write 前に Glob で同名ファイルの存在を確認し、既存なら `_2`, `_3` を付与する。

未同期のミーティングごとに:

1. `mcp__circleback__ReadMeetings` でノート・アクションアイテム・AIインサイト取得（ミーティングIDの配列）
2. `mcp__circleback__GetTranscriptsForMeetings` でトランスクリプト取得（最大50件/バッチ）

以下のテンプレートで `meetings/{YYYY-MM-DD}_{sanitized-name}.md` に Write で書き出す。

ファイル名: 英数字・ハイフン・アンダースコアのみ、スペースはハイフンに、日本語は除去、80文字で切り詰め、小文字。同名は `_2`, `_3` を付与。

```markdown
# {meeting_name}

- **日時**: {date} {start_time} - {end_time}
- **参加者**: {participants をカンマ区切り}
- **時間**: {duration}
- **ソース**: circleback
- **Meeting ID**: {meeting_id}

---

## ノート・ハイライト

{notes / AI insights の内容。なければ「ノートはありません」}

## アクションアイテム

{action items を箇条書き。なければ「アクションアイテムはありません」}

---

## トランスクリプト

{タイムスタンプ付き書き起こし全文。話者名を含む。なければ「トランスクリプトはありません」}
```

## ステップ4: 同期状態の更新

処理完了後、`meetings/_sync-state.json` を更新:

```json
{
  "last_sync": "<現在のISO 8601日時>",
  "synced_meeting_ids": ["既存ID", "新規ID"],
  "provider": "circleback"
}
```

- `synced_meeting_ids` は直近90日分のIDのみ保持する。last_sync より90日以上前のIDは除去する。
- `last_sync` は本日より未来の日付を設定してはならない。

## エラー時

MCP呼び出し失敗時は該当ミーティングをスキップして次へ。スキップ分は `synced_meeting_ids` に追加しない。全件失敗なら `last_sync` を更新しない。
