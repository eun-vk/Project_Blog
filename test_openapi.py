import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Hello, world!"}
        ],
        max_tokens=10,
    )
    print("API 호출 성공:")
    print(response.choices[0].message.content)
except Exception as e:
    print("API 호출 실패:", e)
