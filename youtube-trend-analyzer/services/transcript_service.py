# from youtube_transcript_api import YouTubeTranscriptApi

# def get_transcript(video_id):
#     try:
#         # Create API instance
#         api = YouTubeTranscriptApi()

#         # Fetch transcript (new method)
#         fetched = api.fetch(video_id)

#         # Convert to raw data (list of dicts)
#         transcript = fetched.to_raw_data()

#         # Combine text
#         full_text = " ".join([item["text"] for item in transcript])

#         return full_text

#     except Exception as e:
#         print(f"Transcript not available for video {video_id}: {e}")
#         return None








from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()

        # Try multiple languages
        transcript = api.fetch(video_id, languages=['en', 'hi'])

        full_text = " ".join([item.text for item in transcript])

        return full_text

    except Exception as e:
        print(f"Transcript not available for video {video_id}: {e}")
        return None        