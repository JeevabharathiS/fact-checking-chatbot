from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import ollama
from rag_pipeline import RAGPipeline

app = FastAPI()

MODEL_NAME = "mistral:7b"
rag = RAGPipeline()

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

        # Get the latest user message
        user_message = chat.messages[-1].content if chat.messages else ""

        # Retrieve relevant facts using RAG
        facts = rag.retrieve(user_message, n_results=3)
        context = "\n".join([f"- {fact}" for fact in facts]) if facts else "No relevant facts found."

        # Add a system message with context
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a fact-checking assistant helping people verify information about the current conflict. "
                    "Use the following verified facts to inform your response:\n" + context +
                    "\nProvide accurate, concise answers based on the facts. If no facts are relevant, say so."
                )
            }
        ] + [msg.dict() for msg in chat.messages]

        # Send the full conversation history to Ollama
        response = ollama.chat(model=MODEL_NAME, messages=messages)
        return {"answer": response['message']['content']}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Fact-Checking Chatbot backend is running."}