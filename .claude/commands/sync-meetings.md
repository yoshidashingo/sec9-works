---
description: "Google Driveの議事録を増分同期"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# /sync-meetings - 議事録の増分同期

Google Drive の議事録フォルダから新規・更新されたドキュメントを `meetings/` に同期する。

## 手順

1. 同期スクリプトを実行する

```bash
bash /Users/shingo/Documents/GitHub/sec9-works/.claude/scripts/sync-meetings.sh
```

2. 実行結果のサマリー（新規・更新・スキップ・エラー件数）を表示する
3. エラーがあった場合は原因を調査し、個別にリトライする
4. 新規・更新ファイルがあれば git commit & push する

```bash
cd /Users/shingo/Documents/GitHub/sec9-works
git add meetings/
# 変更がなければスキップ
git diff --cached --quiet || git commit -m "sync: ミーティング議事録の自動同期

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push origin main
```

5. commit & push の結果を報告する

## 補足

- `gws` CLI（Google Workspace CLI）を使用
- `meetings/` 内の最新ファイル日時を基準に増分取得（1日マージン付き）
- 内容が同一のファイルはスキップ
- 対象フォルダ: `1GCMKVhvx0Lrz0H-lN9SyIebu01jEMIAq`（Google Drive「議事録」フォルダ）
