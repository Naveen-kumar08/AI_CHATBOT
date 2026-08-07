from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import ask_ai


app = FastAPI()


class ChatRequest(BaseModel):

    message:str



@app.get("/")
def home():

    return {
        "status":"AI Assistant Backend Running"
    }



@app.post("/chat")
def chat(data:ChatRequest):

    reply = ask_ai(
        data.message
    )

    return {
        "reply":reply
    }