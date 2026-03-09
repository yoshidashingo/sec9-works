#!/usr/bin/env bash
set -euo pipefail
export PATH="/Users/shingo/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:$PATH"

# Claude Codeのネストセッションを回避
unset CLAUDECODE

REPO_DIR="/Users/shingo/Documents/GitHub/sec9-works"
LOG_DIR="$REPO_DIR/logs"
CLAUDE="/Users/shingo/.local/bin/claude"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/sync-paulo_${TIMESTAMP}.log"
PROMPT_FILE="$REPO_DIR/scripts/prompts/sync-paulo.md"
STATE_FILE="$REPO_DIR/output/paulo-newsletter/references/_sync-state.json"

mkdir -p "$LOG_DIR"
cd "$REPO_DIR"

echo "[$(date)] Starting Paulo newsletter sync" >> "$LOG_FILE"

# プロンプトファイル存在チェック
if [ ! -f "$PROMPT_FILE" ]; then
  echo "[$(date)] ERROR: Prompt file not found: $PROMPT_FILE" >> "$LOG_FILE"
  exit 1
fi

# sync-state バリデーション
source "$REPO_DIR/scripts/git-sync-helper.sh"
if ! validate_sync_state "$STATE_FILE" "$LOG_FILE"; then
  echo "[$(date)] ERROR: Invalid sync state, aborting" >> "$LOG_FILE"
  exit 1
fi

$CLAUDE -p "$(cat "$PROMPT_FILE")" \
  --model sonnet \
  --allowedTools "Read,Edit,Write,Glob,ToolSearch,mcp__google-workspace-sec9__search_gmail_messages,mcp__google-workspace-sec9__get_gmail_messages_content_batch,mcp__google-workspace-sec9__get_gmail_message_content" \
  --output-format json \
  --max-turns 15 \
  --max-budget-usd 0.50 \
  >> "$LOG_FILE" 2>&1 || echo "[$(date)] Paulo sync failed" >> "$LOG_FILE"

# sync-state 事後バリデーション（LLMのハルシネーション検出）
if ! validate_sync_state "$STATE_FILE" "$LOG_FILE"; then
  echo "[$(date)] ERROR: LLM corrupted sync state, restoring from git" >> "$LOG_FILE"
  git checkout -- "$STATE_FILE" 2>/dev/null || true
fi

# --- git commit & push ---
git_sync_commit_push \
  "output/paulo-newsletter/" \
  "sync: パウロ メンバーシップ記事の自動同期" \
  "$LOG_FILE" || echo "[$(date)] git sync failed" >> "$LOG_FILE"

# 古いログを削除（30日以上前）
find "$LOG_DIR" -name "sync-paulo_*.log" -type f -mtime +30 -delete
echo "[$(date)] Paulo sync complete" >> "$LOG_FILE"
