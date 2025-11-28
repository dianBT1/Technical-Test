import uuid

class DocumentStore:
    def __init__(self, qdrant, embedding_service):
        self.qdrant = qdrant
        self.embedding_service = embedding_service
        self._docs_memory = []
    
    @property
    def in_memory_count(self):
        return len(self._docs_memory)
    
    def add_document_store(self, text: str):
        doc_id = str(uuid.uuid4())
        emb = self.embedding_service.fake_embed(text)
        
        # Coba Qdrant, kalau gagal pakai memory
        try:
            self.qdrant.upsert_document(
                collection_name=self.qdrant.collection_name,
                id=doc_id,
                vector=emb,
                payload={"text": text}
            )
            print("Document added to Qdrant")
            return {"id": doc_id, "status": "added"}
        except Exception:
            # Fallback ke memory
            print("Document adding to memory")
            self._docs_memory.append(text)
            return {"id": doc_id, "status": "added"}
    
    def search_document_store(self, query: str):
        emb = self.embedding_service.fake_embed(query)
        
        # Coba Qdrant, kalau gagal pakai memory
        try:
            hits = self.qdrant.search_documents(
                collection_name=self.qdrant.collection_name,
                query_vector=emb,
                limit=2
            )
            print("Document searched in Qdrant")
            return [hit.payload["text"] for hit in hits.points]
        except Exception:
            # Fallback ke memory
            print("Document searched in memory")
            results = [doc for doc in self._docs_memory if query.lower() in doc.lower()]
            return results if results else ([self._docs_memory[0]] if self._docs_memory else [])
    