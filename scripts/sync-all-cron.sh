#!/usr/bin/env bash
set -euo pipefail
export PATH="/Users/shingo/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:$PATH"

# sync-all-cron.sh — 全同期スクリプトの順次実行ラッパー
#
# launchd設定（登録済み）:
#   ~/Library/LaunchAgents/com.sec9.sync-all.plist
#   毎日 01:00 に自動実行
#
# 手動登録: launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.sec9.sync-all.plist
# 状態確認: launchctl list | grep sec9.sync-all
# 手動実行: bash /Users/shingo/Documents/GitHub/sec9-works/scripts/sync-all-cron.sh

REPO_DIR="/Users/shingo/Documents/GitHub/sec9-works"
LOCK_FILE="/tmp/sec9-works-sync-all.lock"
LOG_DIR="$REPO_DIR/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/sync-all_${TIMESTAMP}.log"

mkdir -p "$LOG_DIR"

# 重複実行防止
if [ -f "$LOCK_FILE" ]; then
  lock_age=$(( $(date +%s) - $(stat -f %m "$LOCK_FILE") ))
  if [ "$lock_age" -lt 3600 ]; then
    echo "[$(date)] Another sync-all is still running (${lock_age}s old), exiting" >> "$LOG_FILE"
    exit 0
  fi
  echo "[$(date)] WARNING: Stale sync-all lock detected (${lock_age}s old), removing" >> "$LOG_FILE"
  rm -f "$LOCK_FILE"
fi

echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

echo "[$(date)] === Starting all sync jobs ===" >> "$LOG_FILE"

# 1. ミーティング議事録同期（circleback）
echo "[$(date)] --- Running meetings sync ---" >> "$LOG_FILE"
"$REPO_DIR/scripts/sync-meetings-cron.sh" >> "$LOG_FILE" 2>&1 || {
  echo "[$(date)] WARNING: meetings sync exited with error" >> "$LOG_FILE"
}

# 2. Pauloニュースレター同期
echo "[$(date)] --- Running Paulo sync ---" >> "$LOG_FILE"
"$REPO_DIR/scripts/sync-paulo-cron.sh" >> "$LOG_FILE" 2>&1 || {
  echo "[$(date)] WARNING: Paulo sync exited with error" >> "$LOG_FILE"
}

# 3. Market Hack Magazine同期
echo "[$(date)] --- Running Market Hack sync ---" >> "$LOG_FILE"
"$REPO_DIR/scripts/sync-market-hack-cron.sh" >> "$LOG_FILE" 2>&1 || {
  echo "[$(date)] WARNING: Market Hack sync exited with error" >> "$LOG_FILE"
}

echo "[$(date)] === All sync jobs complete ===" >> "$LOG_FILE"

# 古いログを削除（30日以上前）
find "$LOG_DIR" -name "sync-all_*.log" -mtime +30 -delete
