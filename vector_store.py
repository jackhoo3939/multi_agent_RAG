"""
Vector Store Setup for RAG
Creates ChromaDB collections from documents in data/ folders
"""
import os
from pathlib import Path
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VectorStoreManager:
    """Manages ChromaDB vector stores for different agent domains"""

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def load_documents_from_folder(self, folder_path: str) -> List:
        """Load all text documents from a folder"""
        loader = DirectoryLoader(
            folder_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        documents = loader.load()
        return self.text_splitter.split_documents(documents)

    def create_vector_store(self, collection_name: str, documents: List) -> Chroma:
        """Create a ChromaDB vector store from documents"""
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=collection_name,
            persist_directory=self.persist_directory
        )

    def initialize_all_stores(self, data_dir: str = "./data") -> Dict[str, Chroma]:
        """Initialize vector stores for all agent domains"""
        stores = {}
        domains = ["product", "policy", "tech"]

        for domain in domains:
            folder_path = os.path.join(data_dir, domain)
            if os.path.exists(folder_path):
                print(f"Loading documents from {folder_path}...")
                documents = self.load_documents_from_folder(folder_path)
                print(f"Creating vector store for {domain} with {len(documents)} chunks...")
                stores[domain] = self.create_vector_store(
                    collection_name=f"{domain}_collection",
                    documents=documents
                )
                print(f"✓ {domain} vector store created")
            else:
                print(f"⚠ Warning: {folder_path} not found")

        return stores


def setup_vector_stores():
    """Main function to set up all vector stores"""
    manager = VectorStoreManager()
    stores = manager.initialize_all_stores()
    print(f"\n✓ All vector stores initialized: {list(stores.keys())}")
    return stores


if __name__ == "__main__":
    setup_vector_stores()

        return vector_store

    def get_vector_store(self, collection_name: str) -> Chroma:
        """Get existing vector store"""
        return Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
