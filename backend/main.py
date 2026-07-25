from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import get_answer

app = FastAPI()

# Allow our React website (running on a different port) to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # default Vite/React dev server address
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "EchoMe backend is running"}

@app.post("/ask")
def ask(payload: Question):
    result = get_answer(payload.question)
    return result