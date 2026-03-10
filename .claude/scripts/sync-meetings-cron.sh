#!/bin/bash
# sync-meetings-cron.sh - launchd用: 議事録同期 + git commit & push
set -euo pipefail

cd /Users/shingo/Documents/GitHub/sec9-works

echo "=== $(date '+%Y-%m-%d %H:%M:%S') 議事録同期開始 ==="

# 同期実行
bash .claude/scripts/sync-meetings.sh

# git commit & push
git add meetings/
if ! git diff --cached --quiet; then
    git commit -m "sync: ミーティング議事録の自動同期

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
    git push origin main
    echo "commit & push 完了"
else
    echo "変更なし、git操作スキップ"
fi

echo "=== $(date '+%Y-%m-%d %H:%M:%S') 議事録同期完了 ==="
