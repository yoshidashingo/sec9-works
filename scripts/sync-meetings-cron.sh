#!/usr/bin/env bash
set -euo pipefail
export PATH="/Users/shingo/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:$PATH"

# Claude Codeのネストセッションを回避
unset CLAUDECODE

REPO_DIR="/Users/shingo/Documents/GitHub/sec9-works"
LOG_DIR="$REPO_DIR/logs"
CLAUDE="/Users/shingo/.local/bin/claude"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/sync-meetings_${TIMESTAMP}.log"

mkdir -p "$LOG_DIR"
cd "$REPO_DIR"

# git-sync-helper をロード（validate_sync_state 用）
source "$REPO_DIR/scripts/git-sync-helper.sh"

echo "[$(date)] Starting meeting sync" >> "$LOG_FILE"

# --- Sec9 sync (circleback) ---
SEC9_PROMPT="$REPO_DIR/scripts/prompts/sync-sec9.md"
SEC9_STATE="$REPO_DIR/meetings/_sync-state.json"

if [ ! -f "$SEC9_PROMPT" ]; then
  echo "[$(date)] ERROR: Sec9 prompt not found: $SEC9_PROMPT" >> "$LOG_FILE"
else
  if ! validate_sync_state "$SEC9_STATE" "$LOG_FILE"; then
    echo "[$(date)] ERROR: Sec9 sync state invalid, skipping Sec9 sync" >> "$LOG_FILE"
  else
    echo "[$(date)] Starting Sec9 sync" >> "$LOG_FILE"
    $CLAUDE -p "$(cat "$SEC9_PROMPT")" \
      --model sonnet \
      --allowedTools "Read,Write,Glob,ToolSearch,mcp__circleback__SearchMeetings,mcp__circleback__ReadMeetings,mcp__circleback__GetTranscriptsForMeetings,mcp__circleback__SearchTranscripts" \
      --output-format json \
      --max-turns 50 \
      --max-budget-usd 1.00 \
      >> "$LOG_FILE" 2>&1 || echo "[$(date)] Sec9 sync failed" >> "$LOG_FILE"

    # sync-state 事後バリデーション
    if ! validate_sync_state "$SEC9_STATE" "$LOG_FILE"; then
      echo "[$(date)] ERROR: LLM corrupted Sec9 sync state, restoring" >> "$LOG_FILE"
      git checkout -- "$SEC9_STATE" 2>/dev/null || true
    fi
  fi
fi

# --- git commit & push ---
git_sync_commit_push \
  "meetings/" \
  "sync: ミーティング議事録の自動同期" \
  "$LOG_FILE" || echo "[$(date)] git sync failed" >> "$LOG_FILE"

# 古いログを削除（30日以上前）
find "$LOG_DIR" -name "sync-meetings_*.log" -type f -mtime +30 -delete
echo "[$(date)] Sync complete" >> "$LOG_FILE"
