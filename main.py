from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Question(BaseModel):
    student_id: str
    question: str

@app.post("/ask")
def ask_question(data: Question):
    response = openai.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "أنت مساعد لطلاب السادس الاعدادي."},
            {"role": "user", "content": data.question}
        ]
    )
    return {"answer": response.choices[0].message.content}
