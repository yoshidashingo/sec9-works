#!/usr/bin/env bash
# git-sync-helper.sh — cronスクリプト共通のgit操作ヘルパー
#
# 使い方:
#   source scripts/git-sync-helper.sh
#   git_sync_commit_push "output/paulo-newsletter/" "sync: パウロ記事の自動同期" "$LOG_FILE"
#
# 機能:
#   - noclobber によるアトミックなロック取得（TOCTOU 回避）
#   - PID生存チェックによる stale lock 検出
#   - git stash → pull --rebase → stash pop でunstaged changesを安全処理
#   - rebase/stash pop 失敗時は abort して安全に中断
#   - push失敗時は pull --rebase してリトライ（最大3回）
#
# macOS (BSD stat) 専用。Linux では stat -c %Y に変更が必要。

LOCK_FILE="/tmp/sec9-works-git.lock"
LOCK_TIMEOUT=300  # 5分でロックタイムアウト

_log() {
  local log_file="$1"
  shift
  echo "[$(date)] $*" >> "$log_file"
}

_acquire_lock() {
  local log_file="$1"
  local wait_count=0

  while true; do
    # アトミックなロック取得（noclobber）
    if (set -o noclobber; echo $$ > "$LOCK_FILE") 2>/dev/null; then
      _log "$log_file" "Acquired git lock (PID $$)"
      return 0
    fi

    # ロックが既に存在する場合
    if [ -f "$LOCK_FILE" ]; then
      local lock_pid
      lock_pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")

      # PID生存チェック: プロセスが死んでいたら stale lock
      if [ -n "$lock_pid" ] && ! kill -0 "$lock_pid" 2>/dev/null; then
        _log "$log_file" "WARNING: Stale lock detected (PID $lock_pid is dead), removing"
        rm -f "$LOCK_FILE"
        continue
      fi

      # タイムアウト判定
      local lock_age
      lock_age=$(( $(date +%s) - $(stat -f %m "$LOCK_FILE") ))
      if [ "$lock_age" -gt "$LOCK_TIMEOUT" ]; then
        _log "$log_file" "WARNING: Stale lock detected (${lock_age}s old, PID ${lock_pid:-unknown}), removing"
        rm -f "$LOCK_FILE"
        continue
      fi
    fi

    wait_count=$((wait_count + 1))
    if [ "$wait_count" -ge 60 ]; then
      _log "$log_file" "ERROR: Could not acquire git lock after 60 attempts"
      return 1
    fi
    _log "$log_file" "Waiting for git lock... ($wait_count/60)"
    sleep 5
  done
}

_release_lock() {
  local log_file="$1"
  rm -f "$LOCK_FILE"
  _log "$log_file" "Released git lock"
}

# _sync-state.json のバリデーション（呼び出し元から使用可能）
validate_sync_state() {
  local state_file="$1"
  local log_file="$2"

  if [ ! -f "$state_file" ]; then
    return 0  # ファイルなしは正常（初回実行）
  fi

  # JSON構文チェック
  if ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$state_file" 2>/dev/null; then
    _log "$log_file" "ERROR: $state_file is not valid JSON"
    return 1
  fi

  # 日付フィールドの未来日チェック
  local today
  today=$(date +%Y/%m/%d)
  local sync_date
  sync_date=$(python3 -c "
import json,sys
d = json.load(open(sys.argv[1]))
print(d.get('last_sync_date', d.get('last_sync', '')))
" "$state_file" 2>/dev/null || echo "")

  if [ -n "$sync_date" ]; then
    # YYYY/MM/DD or ISO8601 → YYYY/MM/DD に正規化して比較
    local normalized
    normalized=$(echo "$sync_date" | sed 's/-/\//g' | cut -c1-10)
    if [[ "$normalized" > "$today" ]]; then
      _log "$log_file" "ERROR: $state_file has future date: $sync_date (today: $today)"
      return 1
    fi
  fi

  return 0
}

git_sync_commit_push() {
  local add_paths="$1"       # スペース区切りの git add パス
  local commit_msg="$2"      # コミットメッセージ
  local log_file="$3"        # ログファイルパス
  local repo_dir
  repo_dir="${REPO_DIR:-/Users/shingo/Documents/GitHub/sec9-works}"

  cd "$repo_dir"

  # ロック取得
  _acquire_lock "$log_file" || return 1

  # unstaged changes を stash（untracked含む）
  local stashed=false
  if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    _log "$log_file" "Stashing existing changes..."
    git stash push --include-untracked -m "git-sync-helper auto-stash" >> "$log_file" 2>&1 && stashed=true
  fi

  # リモートの変更を取得
  _log "$log_file" "Pulling latest changes..."
  if ! git pull --rebase origin main >> "$log_file" 2>&1; then
    _log "$log_file" "ERROR: git pull --rebase failed, aborting rebase"
    git rebase --abort >> "$log_file" 2>&1 || true
    # stash を復元してから中断
    if [ "$stashed" = true ]; then
      git stash pop >> "$log_file" 2>&1 || true
    fi
    _release_lock "$log_file"
    return 1
  fi

  # stash を復元
  if [ "$stashed" = true ]; then
    _log "$log_file" "Restoring stashed changes..."
    if ! git stash pop >> "$log_file" 2>&1; then
      _log "$log_file" "ERROR: git stash pop failed (conflict). Aborting to prevent data corruption."
      # 競合状態をリセットし、stash はそのまま残す（手動復旧用）
      git checkout -- . >> "$log_file" 2>&1 || true
      _release_lock "$log_file"
      return 1
    fi
  fi

  # 変更をステージング
  # shellcheck disable=SC2086
  git add $add_paths

  if git diff --cached --quiet; then
    _log "$log_file" "No changes to commit"
    _release_lock "$log_file"
    return 0
  fi

  # コミット
  local full_msg
  full_msg="$(cat <<EOF
${commit_msg}

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
  )"
  git commit -m "$full_msg" >> "$log_file" 2>&1
  _log "$log_file" "Committed changes"

  # プッシュ（リトライ付き）
  local retry_count=0
  local max_retries=3
  until git push origin main >> "$log_file" 2>&1; do
    retry_count=$((retry_count + 1))
    if [ $retry_count -ge $max_retries ]; then
      _log "$log_file" "ERROR: Failed to push after $max_retries attempts"
      _release_lock "$log_file"
      return 1
    fi
    _log "$log_file" "Push failed, pulling and retrying ($retry_count/$max_retries)..."
    if ! git pull --rebase origin main >> "$log_file" 2>&1; then
      _log "$log_file" "ERROR: Rebase failed during push retry, aborting"
      git rebase --abort >> "$log_file" 2>&1 || true
      _release_lock "$log_file"
      return 1
    fi
    sleep 3
  done

  _log "$log_file" "Successfully committed and pushed"

  _release_lock "$log_file"
  return 0
}
