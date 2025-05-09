Fact-Checking Chatbot
A fact-checking chatbot to combat war-related propaganda using RAG, Ollama (Mistral 7B), FastAPI, Streamlit, and ChromaDB.
Setup

Create Conda Environment:
conda create -n factcheckbot python=3.10
conda activate factcheckbot
pip install -r requirements.txt


Install Ollama:

Download and install Ollama from ollama.ai.
Pull Mistral 7B:ollama pull mistral:7b




Run the Application:

Start Ollama server:ollama serve


Start FastAPI backend:cd backend
uvicorn main:app --reload


Start Streamlit frontend:cd frontend
streamlit run app.py


Start CMS:cd cms
streamlit run cms.py





Project Structure

backend/: FastAPI backend and RAG pipeline.
frontend/: Streamlit frontend for user interaction.
cms/: Streamlit-based CMS for managing facts.
requirements.txt: Project dependencies.
.env: Configuration file.

Usage

Users: Access the chatbot at http://localhost:8501 to ask war-related questions.
Government Officials: Access the CMS at http://localhost:8502 (or next available port) to manage facts.

