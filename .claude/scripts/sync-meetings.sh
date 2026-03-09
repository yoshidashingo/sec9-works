#!/bin/bash
# sync-meetings.sh - Google Driveの議事録フォルダから増分同期
set -euo pipefail

MEETINGS_DIR="/Users/shingo/Documents/GitHub/sec9-works/meetings"
FOLDER_ID="1GCMKVhvx0Lrz0H-lN9SyIebu01jEMIAq"
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Load GWS credentials from .env.gws
ENV_FILE="/Users/shingo/Documents/GitHub/sec9-works/.env.gws"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
else
    echo "ERROR: $ENV_FILE not found. Create it with GOOGLE_WORKSPACE_CLI_CLIENT_ID and GOOGLE_WORKSPACE_CLI_CLIENT_SECRET."
    exit 1
fi
export GOOGLE_WORKSPACE_CLI_CLIENT_ID
export GOOGLE_WORKSPACE_CLI_CLIENT_SECRET

# 最新ファイルの更新日時を取得（RFC3339形式）
# meetings/内の.mdファイルのうちCLAUDE.md以外で最も新しいもの
LATEST_FILE=$(find "$MEETINGS_DIR" -name '*.md' ! -name 'CLAUDE.md' -type f -exec stat -f '%m %N' {} + 2>/dev/null | sort -rn | head -1 | awk '{print $2}')

if [ -n "$LATEST_FILE" ]; then
    # macOS stat: 秒→RFC3339
    LATEST_EPOCH=$(stat -f '%m' "$LATEST_FILE")
    # 1日前にマージンを取る
    MARGIN_EPOCH=$((LATEST_EPOCH - 86400))
    SINCE=$(date -r "$MARGIN_EPOCH" -u '+%Y-%m-%dT%H:%M:%S.000Z')
    echo "増分同期: $SINCE 以降の更新を取得"
    QUERY="'${FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.document' and modifiedTime > '${SINCE}'"
else
    echo "全件同期: meetingsディレクトリにファイルなし"
    QUERY="'${FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.document'"
fi

# ファイル一覧取得
FILES_JSON=$(gws drive files list --params "{\"q\": \"${QUERY}\", \"pageSize\": 100, \"fields\": \"files(id,name,modifiedTime)\"}" --page-all --page-limit 10 2>/dev/null)

# ファイル数カウント
TOTAL=$(echo "$FILES_JSON" | python3 -c "
import json, sys
files = []
for line in sys.stdin:
    line = line.strip()
    if line:
        data = json.loads(line)
        files.extend(data.get('files', []))
print(len(files))
")

if [ "$TOTAL" -eq 0 ]; then
    echo "新規・更新ファイルはありません"
    exit 0
fi

echo "対象ファイル: ${TOTAL}件"

# エクスポート処理
STATS=$(echo "$FILES_JSON" | python3 -c "
import json, sys
files = []
for line in sys.stdin:
    line = line.strip()
    if line:
        data = json.loads(line)
        files.extend(data.get('files', []))
for f in files:
    print(json.dumps({'id': f['id'], 'name': f['name']}))
" | {
    NEW=0
    UPDATED=0
    SKIPPED=0
    ERRORS=0
    COUNT=0

    while IFS= read -r line; do
        FILE_ID=$(echo "$line" | python3 -c "import json,sys; print(json.loads(sys.stdin.read())['id'])")
        FILE_NAME=$(echo "$line" | python3 -c "import json,sys; print(json.loads(sys.stdin.read())['name'])")

        # ファイル名サニタイズ: / と : を _ に、末尾スペース除去
        SAFE_NAME=$(echo "$FILE_NAME" | sed 's/[\/:]/_/g; s/[[:space:]]*$//')
        OUTPUT_FILE="$MEETINGS_DIR/${SAFE_NAME}.md"

        COUNT=$((COUNT + 1))

        # エクスポート
        cd "$TEMP_DIR"
        rm -f "$TEMP_DIR"/*

        if gws drive files export --params "{\"fileId\": \"$FILE_ID\", \"mimeType\": \"text/plain\"}" --output "$TEMP_DIR/export.txt" 2>/dev/null | grep -q '"success"'; then
            if [ -f "$TEMP_DIR/export.txt" ]; then
                if [ -f "$OUTPUT_FILE" ]; then
                    # 内容比較
                    if diff -q "$TEMP_DIR/export.txt" "$OUTPUT_FILE" >/dev/null 2>&1; then
                        SKIPPED=$((SKIPPED + 1))
                        echo "  [$COUNT/$TOTAL] スキップ(同一): $SAFE_NAME"
                    else
                        mv "$TEMP_DIR/export.txt" "$OUTPUT_FILE"
                        UPDATED=$((UPDATED + 1))
                        echo "  [$COUNT/$TOTAL] 更新: $SAFE_NAME"
                    fi
                else
                    mv "$TEMP_DIR/export.txt" "$OUTPUT_FILE"
                    NEW=$((NEW + 1))
                    echo "  [$COUNT/$TOTAL] 新規: $SAFE_NAME"
                fi
            else
                ERRORS=$((ERRORS + 1))
                echo "  [$COUNT/$TOTAL] エラー: $SAFE_NAME"
            fi
        else
            ERRORS=$((ERRORS + 1))
            echo "  [$COUNT/$TOTAL] エラー: $SAFE_NAME"
        fi

        sleep 0.2
    done

    echo ""
    echo "=== 同期結果 ==="
    echo "新規: ${NEW}件"
    echo "更新: ${UPDATED}件"
    echo "スキップ: ${SKIPPED}件"
    echo "エラー: ${ERRORS}件"
    echo "合計: $(ls "$MEETINGS_DIR"/*.md 2>/dev/null | grep -v CLAUDE.md | wc -l | tr -d ' ')件"
})

echo "$STATS"
