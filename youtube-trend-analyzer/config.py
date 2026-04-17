import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("apies ",YOUTUBE_API_KEY)
print("apies ",GROQ_API_KEY)
