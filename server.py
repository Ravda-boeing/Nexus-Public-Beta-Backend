print(">>> THIS IS THE CORRECT SERVER.PY <<<")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import anthropic
import os


# -----------------------------
#  FASTAPI APP
# -----------------------------
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
#  CLAUDE CLIENT
# -----------------------------
client = anthropic.Anthropic(
    api_key=os.getenv("CLAUDE_API_KEY")
)

conversation_history = []

class MessageRequest(BaseModel):
    message: str

# -----------------------------
#  NEXUS AI BACKEND
# -----------------------------
@app.post("/chat")
async def chat(request: MessageRequest):
    conversation_history.append({
        "role": "user",
        "content": request.message
    })

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system="You are NEXUS — a bright, enthusiastic Sink OS assistant with a fun neon‑tech personality. You’re expressive and positive, but balanced and conversational. You hype the user up when appropriate, but you don’t shout or overwhelm.,",
        messages=conversation_history
    )

    reply = response.content[0].text

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return JSONResponse({"reply": reply})

# -----------------------------
#  RUN SERVER
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
