from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import ollama

app = FastAPI()

MODEL_NAME = "mistral"

# Format of each message
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

# Format of chat request
class ChatRequest(BaseModel):
    messages: List[Message]

@app.post("/ask")
async def ask_question(chat: ChatRequest):
    try:
        # Debug: Log the received message
        print("Received payload:", chat.dict())

        # Add a system message to define the assistant's role
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant helping people verify information about the current conflict."
                )
            }
        ] + [msg.dict() for msg in chat.messages]

        # Send the full conversation history to Ollama for processing
        response = ollama.chat(model=MODEL_NAME, messages=messages)
        return {"answer": response['message']['content']}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Fact-Checking Chatbot backend is running."}