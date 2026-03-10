#!/usr/bin/env python3
"""Gmail からメルマガを取得しマークダウンとして保存する."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import base64
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

import html2text

BASE_DIR = Path("/Users/shingo/Documents/GitHub/sec9-works")
MAGAZINES_DIR = BASE_DIR / "magazines"
STATE_FILE = MAGAZINES_DIR / "_sync-state.json"
ENV_FILE = BASE_DIR / ".env.gws"

# メルマガ定義
SOURCES = [
    {
        "name": "market-hack",
        "label": "Market Hack Magazine",
        "query": 'from:noreply@note.com subject:"Market Hack Magazine"',
        "subject_cleanup": lambda s: re.sub(r"Market Hack Magazine更新のおしらせ", "", s).strip(),
    },
    {
        "name": "paulo",
        "label": "パウロのメルマガ",
        "query": 'from:noreply@note.com "パウロのAIバブルを精査するメンバーシップ"',
        "subject_cleanup": lambda s: s.strip(),
    },
]


def load_env():
    """Load GWS credentials from .env.gws."""
    if not ENV_FILE.exists():
        print(f"ERROR: {ENV_FILE} not found.")
        sys.exit(1)
    env = os.environ.copy()
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def gws_cmd(args: list, env: dict, ndjson: bool = False) -> dict | list:
    """Run a gws command and return parsed JSON.

    If ndjson=True, parse output as NDJSON (one JSON object per line).
    Otherwise, parse as a single JSON object.
    """
    result = subprocess.run(
        ["gws"] + args,
        capture_output=True, text=True, env=env,
    )
    if result.returncode != 0:
        print(f"  gws error: {result.stderr[:200]}")
        return {}
    output = result.stdout.strip()
    if not output:
        return {}
    if not ndjson:
        return json.loads(output)
    # NDJSON: one JSON object per line
    results = []
    for line in output.split("\n"):
        line = line.strip()
        if line and line.startswith("{"):
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return results


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def get_since(state: dict) -> str:
    """Return RFC3339 date string for incremental sync."""
    last_sync = state.get("last_sync")
    if last_sync:
        # Parse and subtract 1 day margin
        dt = datetime.fromisoformat(last_sync.replace("Z", "+00:00"))
        dt -= timedelta(days=1)
        return dt.strftime("%Y/%m/%d")
    # Default: 30 days ago
    dt = datetime.now(timezone.utc) - timedelta(days=30)
    return dt.strftime("%Y/%m/%d")


def extract_html_body(payload: dict) -> str:
    """Extract HTML body from Gmail message payload."""
    mime = payload.get("mimeType", "")
    if "html" in mime and payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
    for part in payload.get("parts", []):
        result = extract_html_body(part)
        if result:
            return result
    return ""


def extract_article_from_html(html: str, source_name: str) -> str:
    """Convert HTML email to markdown, extracting article content."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0  # No wrapping
    h.unicode_snob = True

    md = h.handle(html)

    # Clean up note.com email boilerplate
    lines = md.split("\n")
    cleaned = []
    skip_patterns = [
        r"^サイトで確認する$",
        r"^スキする$",
        r"^スキとは",
        r"^スキはあなたの応援",
        r"^ヘルプ\s*/\s*プライバシー",
        r"^利用規約$",
        r"^noteをご利用いただき",
        r"^参加中のメンバーシップに",
        r"^\[メンバーシップ\]",
        r"^\[プラン\]",
        r"^スタンダートプラン",
        r"^Market Hack Magazineに新しい記事",
        r"^広瀬隆雄\s+Market Hack編集長",
        r"^\*\*メンバーシップ\*\*.*パウロ",
        r"^\*\*プラン\*\*.*スタンダート",
    ]
    in_content = False

    for line in lines:
        stripped = line.strip()
        # Skip empty lines at the start
        if not in_content and not stripped:
            continue
        # Skip boilerplate
        if any(re.match(p, stripped) for p in skip_patterns):
            continue
        # Skip tracking pixels and misc
        if stripped.startswith("![") or "link.note.com" in stripped:
            continue
        in_content = True
        cleaned.append(line)

    # Trim trailing boilerplate and empty lines
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()

    return "\n".join(cleaned).strip()


def extract_subject(headers: list) -> str:
    for h in headers:
        if h["name"] == "Subject":
            return h["value"]
    return "untitled"


def extract_date(headers: list) -> str:
    for h in headers:
        if h["name"] == "Date":
            val = h["value"]
            # Parse email date to YYYY-MM-DD
            for fmt in [
                "%a, %d %b %Y %H:%M:%S %z",
                "%a, %d %b %Y %H:%M:%S %z (%Z)",
                "%d %b %Y %H:%M:%S %z",
            ]:
                try:
                    dt = datetime.strptime(val.strip(), fmt)
                    return dt.strftime("%Y-%m-%d")
                except ValueError:
                    continue
            # Fallback: extract date-like pattern
            m = re.search(r"(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})", val)
            if m:
                month_map = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
                             "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
                return f"{m.group(3)}-{month_map[m.group(2)]}-{int(m.group(1)):02d}"
    return datetime.now().strftime("%Y-%m-%d")


def extract_article_title(md_text: str) -> str:
    """Extract the first H1 heading from markdown as article title."""
    m = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


def sanitize_filename(name: str) -> str:
    """Sanitize string for use in filename."""
    name = re.sub(r'[\/\\:*?"<>|]', '_', name)
    name = re.sub(r'\s+', ' ', name).strip()
    # Truncate to reasonable length
    if len(name) > 80:
        name = name[:80]
    return name


def main():
    env = load_env()
    state = load_state()
    since = get_since(state)

    stats = {"new": 0, "skipped": 0, "errors": 0}

    print(f"増分同期: {since} 以降のメルマガを取得")

    for source in SOURCES:
        query = f'{source["query"]} after:{since}'
        print(f"\n--- {source['label']} ---")
        print(f"  Query: {query}")

        # List messages
        data = gws_cmd([
            "gmail", "users", "messages", "list",
            "--params", json.dumps({"userId": "me", "q": query, "maxResults": 50}),
            "--page-all", "--page-limit", "5",
        ], env, ndjson=True)

        # Collect message IDs from potentially multiple pages
        messages = []
        if isinstance(data, list):
            for page in data:
                messages.extend(page.get("messages", []))
        elif isinstance(data, dict):
            messages = data.get("messages", [])

        if not messages:
            print("  対象メールなし")
            continue

        print(f"  対象: {len(messages)}件")

        for i, msg in enumerate(messages):
            msg_id = msg["id"]

            # Get full message
            full = gws_cmd([
                "gmail", "users", "messages", "get",
                "--params", json.dumps({"userId": "me", "id": msg_id, "format": "full"}),
            ], env)

            if not full:
                stats["errors"] += 1
                print(f"  [{i+1}/{len(messages)}] エラー: メッセージ取得失敗 {msg_id}")
                continue

            headers = full.get("payload", {}).get("headers", [])
            subject = extract_subject(headers)
            date_str = extract_date(headers)

            # Extract and convert content
            html = extract_html_body(full.get("payload", {}))
            if not html:
                stats["errors"] += 1
                print(f"  [{i+1}/{len(messages)}] エラー: HTML本文なし: {subject}")
                continue

            article_md = extract_article_from_html(html, source["name"])

            # Determine article title for filename
            article_title = extract_article_title(article_md)
            clean_subject = article_title or source["subject_cleanup"](subject) or subject

            safe_subject = sanitize_filename(clean_subject)
            filename = f"{date_str}_{source['name']}_{safe_subject}.md"
            output_path = MAGAZINES_DIR / filename

            # Add frontmatter
            content = f"""---
title: "{clean_subject}"
source: {source['label']}
date: {date_str}
gmail_id: {msg_id}
---

{article_md}
"""

            # Check if file exists and content is same
            if output_path.exists():
                existing = output_path.read_text()
                if existing == content:
                    stats["skipped"] += 1
                    print(f"  [{i+1}/{len(messages)}] スキップ(同一): {filename}")
                    continue

            output_path.write_text(content)
            stats["new"] += 1
            print(f"  [{i+1}/{len(messages)}] 保存: {filename}")

    # Update state
    state["last_sync"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    print(f"\n=== 同期結果 ===")
    print(f"新規: {stats['new']}件")
    print(f"スキップ: {stats['skipped']}件")
    print(f"エラー: {stats['errors']}件")
    total = len(list(MAGAZINES_DIR.glob("*.md"))) - 1  # Exclude CLAUDE.md
    print(f"合計: {total}件")

    # Git commit & push if there are new files
    if stats["new"] > 0:
        print("\n--- git commit & push ---")
        os.chdir(BASE_DIR)
        subprocess.run(["git", "add", "magazines/"], check=True)
        result = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if result.returncode != 0:
            subprocess.run([
                "git", "commit", "-m",
                "sync: メルマガの自動同期\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
            ], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("commit & push 完了")
        else:
            print("変更なし、スキップ")
    else:
        print("\n新規ファイルなし、git操作スキップ")


if __name__ == "__main__":
    main()
