import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
class VectorDBTool:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {embedding_model}...")
        self.embedder = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedder.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.documents = []
        print(f"FAISS VectorDB initialized (dim={self.embedding_dim})")
    def add_documents(self, documents):
        if not documents:
            return
        embeddings = self.embedder.encode(documents, convert_to_numpy=True)
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(documents)
        print(f"Added {len(documents)} documents to FAISS")
    def search(self, query, top_k=5):
        if self.count() == 0:
            return []
        query_embedding = self.embedder.encode([query], convert_to_numpy=True)
        k = min(top_k, self.count())
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        results = [self.documents[idx] for idx in indices[0]]
        return results
    def count(self):
        return len(self.documents)
    def clear(self):
        self.index.reset()
        self.documents = []
        print("FAISS database cleared")
