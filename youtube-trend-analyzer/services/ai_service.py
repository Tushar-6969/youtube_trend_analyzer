from groq import Groq
from config import GROQ_API_KEY

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def generate_summary(text):
    if not text.strip():
        return "No transcript data available to analyze."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Analyze the following YouTube video transcripts and provide a clean, readable report.

Rules:
- Use exactly these section titles:
  Main Trending Topics
  Key Insights
  Common Patterns
- Under each section, use short numbered points only.
- Keep the writing concise and professional.
- Do not add any intro sentence like "Based on the transcript".
- Do not use markdown tables.

Text:
{text[:12000]}
"""
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Error in AI processing:", e)
        return "Error generating summary."
