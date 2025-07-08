from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate/")
async def generate_text(data: PromptRequest):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"{data.prompt}에 어울리는 블로그 도입부를 써줘"},
        ],
        max_tokens=300
    )
    return {"result": response.choices[0].message.content}

@app.get("/")
async def root():
    return {"message": "FastAPI 서버가 정상 작동 중입니다."}
