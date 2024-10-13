import numpy as np
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from utils import ensure_loaded 


class NumpyVectorStore:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vectors = None
        self.texts = []
        self.metadatas = []

    def add_documents(self, documents):
        new_texts = [doc.page_content for doc in documents]
        new_metadatas = [doc.metadata for doc in documents]
        new_vectors = self.embedding_model.embed_documents(new_texts)

        if self.vectors is None:
          self.vectors = np.array(new_vectors)
        else:
          self.vectors = np.vstack([self.vectors, new_vectors])

        self.texts.extend(new_texts)
        self.metadatas.extend(new_metadatas)

    def save(self, file_path):
        np.savez(file_path, 
               vectors=self.vectors, 
               texts=np.array(self.texts, dtype=object), 
               metadatas=np.array(self.metadatas, dtype=object))

    @classmethod
    def load(cls, file_path, embedding_model):
        data = np.load(file_path, allow_pickle=True)
        vectorstore = cls(embedding_model)
        vectorstore.vectors = data['vectors']
        vectorstore.texts = data['texts'].tolist()
        vectorstore.metadatas = data['metadatas'].tolist()
        return vectorstore
    
    @ensure_loaded
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        query_vector = self.embedding_model.embed_query(query)

        #cosine similarity
        dot_product = np.dot(self.vectors, query_vector)
        norm = np.linalg.norm(self.vectors, axis=1) * np.linalg.norm(query_vector)
        cosine_similarities = dot_product / norm

        top_k_indices = np.argsort(cosine_similarities)[-k:][::-1]

        results = []
        for idx in top_k_indices:
          doc = Document(
              page_content=self.texts[idx],
              metadata=self.metadatas[idx]
          )
          results.append(doc)

        return results
