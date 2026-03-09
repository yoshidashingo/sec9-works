#!/usr/bin/env python3
"""
Process Circleback meeting data and generate markdown files for Sec9 meetings.
Reads from MCP tool result files and writes individual MD files.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("/Users/shingo/Documents/GitHub/sec9-works/meetings")

# All meeting IDs to process
ALL_MEETING_IDS = [
    6800865, 6784286, 6777182, 6775695, 6773546, 6772476, 6754170, 6742730,
    6718212, 6714774, 6711490, 6695060, 6692841, 6690419, 6689306, 6686700,
    6681264, 6667969, 6666412, 6657212, 6656259, 6655900, 6655223, 6653465,
    6652125, 6637329, 6627744, 6626684, 6624485, 6623543, 6593502, 6551657,
    6549205, 6546986, 6545931, 6536790, 6507918, 6506288, 6505578, 6502476,
    6478165, 6477417, 6475164, 6474266, 6456640, 6450947, 6444550, 6419843,
    6416518, 6414149, 6413174, 6394865, 6392267, 6391449, 6382724, 6354843,
    6353238, 6352602, 6333526, 6325476, 6324663, 6303681, 6274485, 6267334,
    6264630, 6260713, 6239862, 6205917, 6203919, 6202111, 6199173, 6198997
]


def sanitize_filename(name: str) -> str:
    """Sanitize meeting name for filename: keep alphanumeric, hyphens, underscores.
    Remove Japanese chars. Spaces become hyphens. Lowercase. Truncate at 80 chars."""
    if not name:
        return "untitled-meeting"
    # Remove Japanese characters (Hiragana, Katakana, CJK Unified Ideographs, etc.)
    name = re.sub(r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff\uff00-\uffef\u2000-\u206f]', '', name)
    # Replace spaces, dots, colons with hyphens
    name = re.sub(r'[\s.:/\\]+', '-', name)
    # Keep only alphanumeric, hyphens, underscores
    name = re.sub(r'[^a-zA-Z0-9\-_]', '', name)
    # Collapse multiple hyphens
    name = re.sub(r'-+', '-', name)
    # Strip leading/trailing hyphens
    name = name.strip('-_')
    # Lowercase
    name = name.lower()
    # Truncate
    if len(name) > 80:
        name = name[:80].rstrip('-_')
    if not name:
        return "untitled-meeting"
    return name


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string."""
    if not seconds:
        return "不明"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    if minutes >= 60:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}時間{mins}分{secs}秒"
    return f"{minutes}分{secs}秒"


def format_timestamp(seconds: float) -> str:
    """Format seconds to HH:MM:SS or MM:SS."""
    if seconds is None:
        return ""
    total_secs = int(seconds)
    hours = total_secs // 3600
    mins = (total_secs % 3600) // 60
    secs = total_secs % 60
    if hours > 0:
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def get_unique_filepath(base_path: Path) -> Path:
    """If file exists, append _2, _3, etc."""
    if not base_path.exists():
        return base_path
    stem = base_path.stem
    suffix = base_path.suffix
    counter = 2
    while True:
        new_path = base_path.parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def format_attendees(attendees: list) -> str:
    """Format attendees list, skip null names."""
    names = []
    for a in attendees:
        name = a.get("name")
        if name:
            names.append(name)
    if not names:
        return "不明"
    return ", ".join(names)


def format_notes(meeting: dict) -> str:
    """Format notes and AI insights."""
    parts = []
    notes = meeting.get("notes", "")
    if notes:
        parts.append(notes)

    insights = meeting.get("insights", {})
    if insights:
        for key, items in insights.items():
            if key == "Follow-up email":
                continue  # Skip follow-up emails in notes section
            if items:
                for item in items:
                    insight_text = item.get("insight", "")
                    if insight_text:
                        parts.append(f"\n### {key}\n\n{insight_text}")

    if not parts:
        return "ノートはありません"
    return "\n\n".join(parts)


def format_action_items(items: list) -> str:
    """Format action items as bullet list."""
    if not items:
        return "アクションアイテムはありません"
    lines = []
    for item in items:
        title = item.get("title", "")
        desc = item.get("description", "")
        assignee = item.get("assignee")
        status = item.get("status", "")
        assignee_name = ""
        if assignee:
            assignee_name = assignee.get("name") or assignee.get("email") or ""

        line = f"- **{title}**"
        if desc:
            line += f": {desc}"
        if assignee_name:
            line += f" (担当: {assignee_name})"
        if status:
            line += f" [{status}]"
        lines.append(line)
    return "\n".join(lines)


def format_transcript(transcript_data: dict) -> str:
    """Format transcript segments with timestamps and speaker names."""
    if not transcript_data:
        return "トランスクリプトはありません"

    segments = transcript_data.get("transcript", [])
    if not segments:
        return "トランスクリプトはありません"

    lines = []
    for seg in segments:
        start = format_timestamp(seg.get("startTimestamp"))
        speaker = seg.get("speaker", "不明")
        words = seg.get("words", "")
        if start:
            lines.append(f"**[{start}] {speaker}**: {words}")
        else:
            lines.append(f"**{speaker}**: {words}")

    if not lines:
        return "トランスクリプトはありません"
    return "\n\n".join(lines)


def parse_datetime(dt_str: str):
    """Parse ISO datetime string."""
    if not dt_str:
        return None
    # Handle various formats
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        try:
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except (ValueError, AttributeError):
            return None


def generate_md(meeting: dict, transcript_data: dict = None) -> str:
    """Generate markdown content for a meeting."""
    name = meeting.get("name", "Untitled Meeting")
    created_at = meeting.get("createdAt", "")
    duration = meeting.get("duration", 0)
    attendees = meeting.get("attendees", [])
    action_items = meeting.get("actionItems", [])
    meeting_id = meeting.get("id", "")

    dt = parse_datetime(created_at)
    date_str = dt.strftime("%Y-%m-%d") if dt else "不明"
    time_str = dt.strftime("%H:%M") if dt else "不明"

    # Estimate end time from duration
    if dt and duration:
        from datetime import timedelta
        end_dt = dt + timedelta(seconds=duration)
        end_time_str = end_dt.strftime("%H:%M")
    else:
        end_time_str = "不明"

    attendees_str = format_attendees(attendees)
    duration_str = format_duration(duration)
    notes_str = format_notes(meeting)
    action_items_str = format_action_items(action_items)
    transcript_str = format_transcript(transcript_data)

    md = f"""# {name}

- **日時**: {date_str} {time_str} - {end_time_str}
- **参加者**: {attendees_str}
- **時間**: {duration_str}
- **ソース**: circleback
- **Meeting ID**: {meeting_id}

---

## ノート・ハイライト

{notes_str}

## アクションアイテム

{action_items_str}

---

## トランスクリプト

{transcript_str}
"""
    return md


def load_tool_result(filepath: str) -> list:
    """Load and parse a tool result file. Returns list of meeting/transcript objects."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    # Format is: [{"type": "text", "text": "...json..."}]
    if isinstance(raw, list) and len(raw) > 0:
        text_content = raw[0].get("text", "")
        if text_content:
            try:
                return json.loads(text_content)
            except json.JSONDecodeError:
                # Maybe the text is the data directly
                return raw
    return raw


def find_tool_result_files(base_dir: str) -> dict:
    """Find all relevant tool result files."""
    results = {
        "meetings": [],
        "transcripts": []
    }
    for f in os.listdir(base_dir):
        full_path = os.path.join(base_dir, f)
        if "ReadMeetings" in f and f.endswith(".txt"):
            results["meetings"].append(full_path)
        elif "GetTranscriptsForMeetings" in f and f.endswith(".txt"):
            results["transcripts"].append(full_path)
    return results


def main():
    tool_results_dir = "/Users/shingo/.claude/projects/-Users-shingo-github-assessment/fb22eca9-2b81-4016-b69e-5294037b5228/tool-results"

    # Ensure output dir exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Find and load all tool result files
    result_files = find_tool_result_files(tool_results_dir)

    print(f"Found {len(result_files['meetings'])} meeting files, {len(result_files['transcripts'])} transcript files")

    # Load all meetings
    all_meetings = {}
    for mf in result_files["meetings"]:
        print(f"Loading meetings from: {os.path.basename(mf)}")
        try:
            meetings = load_tool_result(mf)
            if isinstance(meetings, list):
                for m in meetings:
                    mid = m.get("id")
                    if mid:
                        all_meetings[mid] = m
        except Exception as e:
            print(f"  Error loading {mf}: {e}")

    print(f"Loaded {len(all_meetings)} unique meetings")

    # Load all transcripts
    all_transcripts = {}
    for tf in result_files["transcripts"]:
        print(f"Loading transcripts from: {os.path.basename(tf)}")
        try:
            transcripts = load_tool_result(tf)
            if isinstance(transcripts, list):
                for t in transcripts:
                    mid = t.get("meetingId")
                    if mid:
                        all_transcripts[mid] = t
        except Exception as e:
            print(f"  Error loading {tf}: {e}")

    print(f"Loaded {len(all_transcripts)} unique transcripts")

    # Process each meeting
    success_ids = []
    failed_ids = []
    used_filenames = set()

    # Also check existing files
    for existing in OUTPUT_DIR.iterdir():
        if existing.is_file() and existing.suffix == ".md":
            used_filenames.add(existing.stem)

    for mid in ALL_MEETING_IDS:
        try:
            meeting = all_meetings.get(mid)
            if not meeting:
                print(f"  WARNING: Meeting {mid} not found in loaded data")
                failed_ids.append((mid, "Meeting data not found"))
                continue

            transcript = all_transcripts.get(mid)

            # Generate filename
            created_at = meeting.get("createdAt", "")
            dt = parse_datetime(created_at)
            date_prefix = dt.strftime("%Y-%m-%d") if dt else "unknown-date"
            name_part = sanitize_filename(meeting.get("name", ""))
            base_stem = f"{date_prefix}_{name_part}"

            # Ensure unique filename
            stem = base_stem
            counter = 2
            while stem in used_filenames:
                stem = f"{base_stem}_{counter}"
                counter += 1
            used_filenames.add(stem)

            filepath = OUTPUT_DIR / f"{stem}.md"

            # Generate and write MD
            md_content = generate_md(meeting, transcript)
            filepath.write_text(md_content, encoding='utf-8')

            print(f"  OK: {mid} -> {filepath.name}")
            success_ids.append(mid)

        except Exception as e:
            print(f"  FAIL: {mid} -> {e}")
            failed_ids.append((mid, str(e)))

    # Summary
    print("\n" + "=" * 60)
    print(f"SUMMARY: {len(success_ids)} succeeded, {len(failed_ids)} failed out of {len(ALL_MEETING_IDS)} total")
    if success_ids:
        print(f"\nSuccessful IDs: {', '.join(str(x) for x in success_ids)}")
    if failed_ids:
        print(f"\nFailed IDs:")
        for fid, reason in failed_ids:
            print(f"  {fid}: {reason}")

    # Remove placeholder file if it exists
    placeholder = OUTPUT_DIR / "placeholder"
    if placeholder.exists():
        placeholder.unlink()


if __name__ == "__main__":
    main()
