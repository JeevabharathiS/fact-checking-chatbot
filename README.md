# Fact-Checking Chatbot

A fact-checking chatbot to combat misinformation about the 2025 India-Pakistan conflict, including the Pahalgam attack and Operation Sindoor. Built with FastAPI, Streamlit, ChromaDB, and Ollama (Mistral model), it uses a Retrieval-Augmented Generation (RAG) pipeline to provide verified answers from a curated dataset.

## Purpose

The chatbot verifies facts related to conflict events, debunking fake news (e.g., false claims of Pakistani strikes) to promote accurate information. It aligns with:
- **SDG 16 (Peace, Justice)**: Counters misinformation to foster peace and trust (Target 16.10).
- **SDG 4 (Education)**: Enhances media literacy by providing verified facts (Target 4.7).
- **SDG 10 (Inclusion)**: Ensures accessible fact-checking for all (Target 10.2).
- **SDG 17 (Partnerships)**: Leverages technology for sustainable development (Target 17.8).

## Prerequisites

- **OS**: Windows 10/11.
- **Hardware**: NVIDIA GPU (e.g., RTX 3060, ≥6 GB VRAM) for Ollama acceleration.
- **Software**:
  - Miniconda/Anaconda.
  - NVIDIA CUDA Toolkit 12.x and cuDNN (for GPU support).
  - Git.
- **Dependencies**: Listed in `requirements.txt` (FastAPI, Streamlit, ChromaDB, etc.).
- **Dataset**: `backend/data/war_data.yaml` (66 verified facts about the 2025 conflict).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd fact-checking-chatbot
   ```

2. **Set Up Conda Environment**:
   ```bash
   conda create -n factchat python=3.11
   conda activate factchat
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama**:
   - Download and install Ollama from [ollama.ai](https://ollama.ai/download).
   - Pull the Mistral model:
     ```bash
     ollama pull mistral
     ```

5. **Install CUDA (for GPU Acceleration)**:
   - Download CUDA Toolkit 12.x from [NVIDIA](https://developer.nvidia.com/cuda-downloads).
   - Install cuDNN (requires NVIDIA Developer account) and copy files to CUDA directories.
   - Verify:
     ```bash
     nvidia-smi
     nvcc --version
     ```

6. **Prepare Dataset**:
   - Ensure `backend/data/war_data.yaml` contains the verified facts (provided separately).
   - Example entry:
     ```yaml
     - date: '2025-04-22'
       fact: 'On April 22, 2025, a terrorist attack in Pahalgam, Jammu and Kashmir, killed 26 civilians...'
       source: Government of India Press Release
     ```

## Running the Chatbot

1. **Start Ollama Server** (in a terminal):
   ```bash
   set CUDA_VISIBLE_DEVICES=0
   ollama serve
   ```

2. **Run Backend** (in a new terminal):
   ```bash
   conda activate factchat
   cd C:\Users\Jeevabharathi\What's Cookin\fact-checking-chatbot
   uvicorn backend.main:app --reload
   ```
   - Access at `http://127.0.0.1:8000/health` to verify.

3. **Run Frontend** (in a new terminal):
   ```bash
   conda activate factchat
   cd C:\Users\Jeevabharathi\What's Cookin\fact-checking-chatbot\frontend
   streamlit run app.py
   ```
   - Access at `http://localhost:8501`.

4. **Run CMS (Optional, for Fact Management)**:
   ```bash
   conda activate factchat
   cd C:\Users\Jeevabharathi\What's Cookin\fact-checking-chatbot\cms
   streamlit run cms.py
   ```
   - Access at `http://localhost:8502`.
   - Log in with credentials from `.streamlit/secrets.toml` (e.g., username: `admin`, password: `securepassword123`).

## Usage

### Querying Facts (Frontend)
- Open `http://localhost:8501`.
- Enter queries like:
  - “What happened in the Pahalgam attack?”
  - “Did Pakistan shoot down Rafale jets?”
  - “What is S. Jaishankar saying?”
- Expected output: Conversational responses (e.g., “On April 22, 2025, a terrorist attack in Pahalgam killed 26 civilians...”).
- Check logs in `chatbot.log` for query details.

### Managing Facts (CMS)
- Open `http://localhost:8502`.
- Log in and upload/edit `war_data.yaml` to update facts.
- Reload data via backend:
  ```bash
  curl -X POST http://127.0.0.1:8000/reload-data
  ```

## File Structure

```
fact-checking-chatbot/
├── backend/
│   ├── main.py           # FastAPI backend with RAG pipeline
│   ├── rag_pipeline.py   # RAG logic for fact retrieval
│   ├── data/
│   │   └── war_data.yaml # Verified facts dataset
├── frontend/
│   └── app.py            # Streamlit frontend for user queries
├── cms/
│   └── cms.py           # Streamlit CMS for fact management
├── .streamlit/
│   └── secrets.toml      # CMS credentials
├── requirements.txt      # Dependencies
├── chatbot.log           # Query and response logs
└── README.md             # Project documentation
```

## Troubleshooting

- **Ollama Not Using GPU**:
  - Verify CUDA:
    ```bash
    nvidia-smi
    ```
  - Ensure `CUDA_VISIBLE_DEVICES=0` is set before `ollama serve`.
  - If slow, try a smaller model:
    ```bash
    ollama pull mistral:7b-q2_K
    ```
    Update `backend/main.py`: `MODEL_NAME = "mistral:7b-q2_K"`.

- **Backend Errors**:
  - Check `http://127.0.0.1:8000/health`.
  - Ensure Ollama is running (`ollama serve`).
  - Verify `war_data.yaml` is valid YAML.

- **Frontend Output Issues**:
  - If responses are not conversational, check `frontend/app.py` rendering.
  - Ensure backend returns `{"answer": "..."}` (test with `curl -X POST http://127.0.0.1:8000/ask`).

- **CMS Login Fails**:
  - Verify `.streamlit/secrets.toml` credentials.
  - Default: `username = "admin"`, `password = "securepassword123"`.

## Contributing

- Fork the repository.
- Create a branch (`git checkout -b feature/new-feature`).
- Commit changes (`git commit -m "Add new feature"`).
- Push (`git push origin feature/new-feature`).
- Open a pull request.
