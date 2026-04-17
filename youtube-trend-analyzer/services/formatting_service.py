import html
import re


NOISE_PATTERNS = [
    r"http[s]?://\S+",
    r"www\.\S+",
    r"\d{1,2}:\d{2}(?:\s*-\s*[A-Za-z].*?)?(?=\s|$)",
]

TRUNCATE_MARKERS = [
    "CHAPTERS",
    "About Me",
    "Instagram:",
    "Twitter:",
    "LinkedIn:",
    "Join",
    "Please leave a LIKE",
    "Books You Should Read",
    "Tech I use every day",
    "Tags",
    "Hashtags",
]


def clean_video_text(text, limit=650):
    if not text:
        return ""

    cleaned = text.replace("\n", " ")

    for marker in TRUNCATE_MARKERS:
        if marker.lower() in cleaned.lower():
            cleaned = re.split(re.escape(marker), cleaned, flags=re.IGNORECASE)[0]
            break

    for pattern in NOISE_PATTERNS:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)

    cleaned = re.sub(r"[#@][\w-]+", " ", cleaned)
    cleaned = re.sub(r"[^\w\s.,!?():/\-']", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -,.")

    if len(cleaned) <= limit:
        return cleaned

    shortened = cleaned[:limit].rsplit(" ", 1)[0].strip()
    return shortened + "..."


def build_video_preview(video, transcript_text):
    cleaned_transcript = clean_video_text(transcript_text or "", limit=900)
    cleaned_description = clean_video_text(video.get("desc", ""), limit=500)

    if cleaned_transcript and len(cleaned_transcript) > 140:
        preview = cleaned_transcript
        source = "Transcript"
        content_for_ai = cleaned_transcript
    else:
        preview = cleaned_description or "No transcript or usable description was available."
        source = "Description"
        content_for_ai = f"{video.get('title', '')}. {cleaned_description}".strip()

    return {
        "preview": preview,
        "source": source,
        "content_for_ai": content_for_ai,
    }


def format_ai_response(text):
    if not text or not text.strip():
        return "<p>No AI summary available.</p>"

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines and lines[0].lower().startswith("based on"):
        lines = lines[1:]

    blocks = []
    current_items = []

    def flush_list():
        nonlocal current_items
        if current_items:
            items_html = "".join(f"<li>{html.escape(item)}</li>" for item in current_items)
            blocks.append(f"<ul class='summary-list'>{items_html}</ul>")
            current_items = []

    for line in lines:
        normalized = re.sub(r"^\*\*(.+?)\*\*$", r"\1", line)
        normalized = re.sub(r"^\*\*(.+?)\*\*:?$", r"\1", normalized).strip()

        if re.match(r"^(main trending topics|key insights|common patterns)\s*:?$", normalized, re.IGNORECASE):
            flush_list()
            blocks.append(f"<h3>{html.escape(normalized.rstrip(':'))}</h3>")
            continue

        bullet_match = re.match(r"^(?:[-*•]|\d+\.)\s+(.*)", line)
        if bullet_match:
            current_items.append(bullet_match.group(1).strip())
            continue

        flush_list()
        blocks.append(f"<p>{html.escape(normalized)}</p>")

    flush_list()
    return "".join(blocks)
