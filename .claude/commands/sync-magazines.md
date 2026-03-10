---
description: "Gmailのメルマガを増分同期"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# /sync-magazines - メルマガの増分同期

Gmail から Market Hack Magazine とパウロのメルマガを `magazines/` に同期する。

## 手順

1. 同期スクリプトを実行する

```bash
python3 /Users/shingo/Documents/GitHub/sec9-works/.claude/scripts/sync-magazines.py
```

2. 実行結果のサマリー（新規・スキップ・エラー件数）を表示する
3. エラーがあった場合は原因を調査し、個別にリトライする
4. 新規・更新ファイルがあれば git commit & push する

```bash
cd /Users/shingo/Documents/GitHub/sec9-works
git add magazines/
# 変更がなければスキップ
git diff --cached --quiet || git commit -m "sync: メルマガの自動同期

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push origin main
```

5. commit & push の結果を報告する

## 補足

- `gws` CLI（Google Workspace CLI）でGmail APIを使用
- `magazines/_sync-state.json` で最終同期日時を管理（初回は30日前から取得）
- HTML メールを html2text でマークダウンに変換
- note.com のメール通知テンプレートのボイラープレートは除去
