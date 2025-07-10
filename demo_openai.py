import openai

prompt = "우리는 무엇으로 사는가"

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": f"{prompt}에 어울리는 블로그 도입부를 써줘"},
    ],
    max_tokens=300,
)
result_text = response.choices[0].message.content  # 1.x 이상
print(f"OpenAI 응답: {result_text}")
