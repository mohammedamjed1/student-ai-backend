from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# الحصول على مفتاح OpenAI من Environment
openai.api_key = os.getenv("OPENAI_API_KEY")

class Question(BaseModel):
    student_id: str
    question: str

app = FastAPI()

# تفعيل CORS للسماح للواجهة بالاتصال
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقًا ضع رابط موقعك فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(q: Question):
    try:
        completion = openai.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": q.question}]
        )
        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        # يطبع الخطأ في اللوج ويسمح للواجهة بعرض رسالة
        print("Error:", e)
        return {"answer": f"حدث خطأ داخلي، حاول لاحقاً."}
