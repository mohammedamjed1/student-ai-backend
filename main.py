from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

# إذا أردت استخدام OpenAI API
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# تفعيل CORS للسماح للواجهة بالاتصال
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقًا ضع رابط موقعك فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# نموذج بيانات السؤال
class Question(BaseModel):
    student_id: str
    question: str

# صفحة HTML رئيسية
@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <html>
      <head>
        <title>مساعد طلاب السادس</title>
      </head>
      <body>
        <h1>مرحبًا بطلاب السادس الاعدادي</h1>
        <form id="askForm">
          <input type="text" id="question" placeholder="اكتب سؤالك هنا" size="50">
          <button type="button" onclick="ask()">اسأل</button>
        </form>
        <p id="answer"></p>
        <script>
          async function ask() {
            let q = document.getElementById("question").value;
            let res = await fetch("/ask", {
              method: "POST",
              headers: {"Content-Type":"application/json"},
              body: JSON.stringify({student_id:"test", question:q})
            });
            let data = await res.json();
            document.getElementById("answer").innerText = data.answer;
          }
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Endpoint لأسئلة الطلاب
@app.post("/ask")
def ask_question(data: Question):
    try:
        # هنا نستخدم GPT-5-mini
        response = openai.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد لطلاب السادس الاعدادي."},
                {"role": "user", "content": data.question}
            ]
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        print("Error:", e)
        return {"answer": "حدث خطأ داخلي، حاول لاحقاً."}
