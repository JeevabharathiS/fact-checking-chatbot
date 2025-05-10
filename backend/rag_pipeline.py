import chromadb
import yaml
import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RAGPipeline:
    def __init__(self, data_path="backend/data/war_data.yaml", db_path="chroma_db"):
        self.data_path = data_path
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)

        collection_exists = any(col.name == "war_facts" for col in self.client.list_collections())
        if collection_exists:
            self.client.delete_collection(name="war_facts")
            logging.info("Deleted existing ChromaDB collection: war_facts")
        self.collection = self.client.create_collection(name="war_facts")
        logging.info("Initialized new ChromaDB collection: war_facts")
        self.load_data()

    def load_data(self):
        logging.info(f"Loading data from {self.data_path}")
        if not os.path.exists(self.data_path):
            logging.warning(f"No data file found at {self.data_path}. Creating empty file.")
            with open(self.data_path, 'w') as f:
                yaml.dump([], f)
            return

        try:
            with open(self.data_path, 'r') as f:
                data = yaml.safe_load(f) or []
        except Exception as e:
            logging.error(f"Failed to load YAML file: {e}")
            return


        try:
            for i, item in enumerate(data):
                if not isinstance(item, dict) or 'fact' not in item:
                    logging.warning(f"Skipping invalid item at index {i}: {item}")
                    continue
                self.collection.add(
                    documents=[item['fact']],
                    metadatas=[{"source": item.get("source", "unknown"), "date": item.get("date", "")}],
                    ids=[str(i)]
                )
            logging.info(f"Indexed {len(data)} facts in ChromaDB.")
        except Exception as e:
            logging.error(f"Failed to index data in ChromaDB: {e}")
            return

    def retrieve(self, query, n_results=3):
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            logging.info(f"Retrieved {len(results['documents'][0])} facts for query: {query}")
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logging.error(f"Query failed: {e}")
            return []