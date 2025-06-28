# services/summarizer.py
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # 환경변수에서 가져오기

def summarize_text(text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes cryptocurrency YouTube transcripts."},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message["content"]
