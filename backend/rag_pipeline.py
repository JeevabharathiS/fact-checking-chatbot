import chromadb
import yaml
import os
from pathlib import Path

class RAGPipeline:
    def __init__(self, data_path="backend/data/war_data.yaml", db_path="chroma_db"):
        self.data_path = data_path
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="war_facts")
        self.load_data()

    def load_data(self):
        """Load and index war-related facts from YAML file."""
        if not os.path.exists(self.data_path):
            print(f"No data file found at {self.data_path}. Creating empty file.")
            with open(self.data_path, 'w') as f:
                yaml.dump([], f)
            return

        with open(self.data_path, 'r') as f:
            data = yaml.safe_load(f) or []

        # Clear existing data in collection
        self.collection.delete(where={})

        # Index new data
        for i, item in enumerate(data):
            if not isinstance(item, dict) or 'fact' not in item:
                continue
            self.collection.add(
                documents=[item['fact']],
                metadatas=[{"source": item.get("source", "unknown"), "date": item.get("date", "")}],
                ids=[str(i)]
            )
        print(f"Indexed {len(data)} facts in ChromaDB.")

    def retrieve(self, query, n_results=3):
        """Retrieve relevant facts for a given query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []