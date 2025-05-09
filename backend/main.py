from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import ollama
from backend.rag_pipeline import RAGPipeline
import logging

logging.basicConfig(filename='chatbot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

app = FastAPI()

MODEL_NAME = "mistral"
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
        logging.info(f"User query: {chat.messages[-1].content}")

        # Get the latest user message
        user_message = chat.messages[-1].content if chat.messages else ""

        # Retrieve relevant facts using RAG
        facts = rag.retrieve(user_message, n_results=3)
        context = "\n".join([f"- {fact}" for fact in facts]) if facts else "No relevant facts found."
        logging.info(f"Retrieved facts: {context}")

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
        try:
            response = ollama.chat(model=MODEL_NAME, messages=messages)
            logging.info(f"Ollama response: {response['message']['content'][:100]}...")
            return {"answer": response['message']['content']}
        except Exception as e:
            logging.error(f"Ollama API error: {str(e)}")
            return {"error": f"Failed to get response from language model: {str(e)}"}

    except Exception as e:
        logging.error(f"General error: {str(e)}")
        return {"error": str(e)}

@app.post("/reload-data")
async def reload_data():
    try:
        rag.load_data()
        logging.info("Data reloaded successfully")
        return {"message": "Data reloaded successfully."}
    except Exception as e:
        logging.error(f"Data reload error: {str(e)}")
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Fact-Checking Chatbot backend is running."}

@app.get("/health")
async def health_check():
    try:
        ollama.list()  # Check if Ollama is reachable
        return {"status": "healthy", "ollama": "running", "model": MODEL_NAME}
    except Exception as e:
        return {"status": "unhealthy", "ollama": str(e)}