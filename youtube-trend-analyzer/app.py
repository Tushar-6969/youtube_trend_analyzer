from flask import Flask, render_template, request
from services.youtube_service import fetch_videos
from services.transcript_service import get_transcript
from services.ai_service import generate_summary
from services.formatting_service import build_video_preview, format_ai_response
import time

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    query = request.form.get("query")
    limit = request.form.get("limit")

    if not query:
        return "Error: Query is required"

    try:
        limit = int(limit)
    except Exception:
        limit = 5

    if limit > 10:
        limit = 10

    videos = fetch_videos(query, limit)

    all_text = ""
    valid_videos = []

    print(f"\nTotal videos fetched: {len(videos)}\n")

    for video in videos:
        video_id = video["video_id"]
        print(f"Processing video: {video_id}")

        transcript_text = get_transcript(video_id)
        preview_data = build_video_preview(video, transcript_text)

        if transcript_text and len(transcript_text) > 100:
            print(f"Transcript length: {len(transcript_text)}")
        else:
            print("Using cleaned fallback description")

        all_text += (
            f"Video Title: {video['title']}\n"
            f"Source Used: {preview_data['source']}\n"
            f"Content: {preview_data['content_for_ai']}\n\n"
        )

        prepared_video = dict(video)
        prepared_video["preview"] = preview_data["preview"]
        prepared_video["content_source"] = preview_data["source"]
        valid_videos.append(prepared_video)

        time.sleep(1.5)

    if all_text.strip():
        summary = generate_summary(all_text)
    else:
        summary = "No usable content available."

    summary_html = format_ai_response(summary)

    total_videos = len(videos)
    analyzed_videos = len(valid_videos)

    print(f"\nAnalyzed {analyzed_videos} / {total_videos} videos\n")

    return render_template(
        "result.html",
        videos=valid_videos,
        summary=summary,
        summary_html=summary_html,
        total=total_videos,
        analyzed=analyzed_videos,
    )


if __name__ == "__main__":
    app.run(debug=True)
