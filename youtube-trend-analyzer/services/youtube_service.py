# import requests
# from config import YOUTUBE_API_KEY

# def fetch_videos(query, limit):
#     url = "https://www.googleapis.com/youtube/v3/search"

#     params = {
#         "part": "snippet",
#         "q": query,
#         "key": YOUTUBE_API_KEY,
#         "maxResults": limit,
#         "type": "video"
#     }

#     response = requests.get(url, params=params)
#     data = response.json()

#     videos = []

#     for item in data.get("items", []):
#         video = {
#             "title": item["snippet"]["title"],
#             "desc": item["snippet"]["description"],
#             "video_id": item["id"]["videoId"]
#         }
#         videos.append(video)

#     return videos


import requests
from config import YOUTUBE_API_KEY

def fetch_videos(query, limit):
    search_url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": limit,
        "type": "video"
    }

    res = requests.get(search_url, params=params).json()

    video_ids = [item["id"]["videoId"] for item in res["items"]]

    # 🔥 SECOND API CALL (IMPORTANT)
    details_url = "https://www.googleapis.com/youtube/v3/videos"

    details_params = {
        "part": "snippet",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY
    }

    details_res = requests.get(details_url, params=details_params).json()

    videos = []

    for item in details_res["items"]:
        videos.append({
            "title": item["snippet"]["title"],
            "desc": item["snippet"]["description"],  # FULL DESCRIPTION
            "video_id": item["id"]
        })

    return videos