from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from typing import List


class QdrantClientService:
    def __init__(self):
        self.collection_name = "demo_collection"
        self._is_ready = False # Status internal
        self._client = None

        try:
            # init client
            self._client = QdrantClient("http://localhost:6333")
            # ensure collection exists
            self._ensure_collection_exists()
            # set status to ready
            self._is_ready = True
        except Exception as e:
            # set status to not ready
            print(f"⚠️  Failed to initialize Qdrant client: {e}")
            self._is_ready = False
    
    def is_available(self):
        return self._is_ready
    
    def _try_reconnect(self):
        """Coba reconnect jika down."""
        if self._is_ready:
            return True
        
        try:
            if self._client is None:
                self._client = QdrantClient("http://localhost:6333")
            self._client.get_collection(self.collection_name)
            self._ensure_collection_exists()
            self._is_ready = True
            return True
        except Exception:
            self._is_ready = False
            return False
    
    def _ensure_ready(self):
        """Pastikan Qdrant ready, coba reconnect jika perlu. Raise exception jika gagal."""
        if not self._is_ready:
            self._try_reconnect()
        if not self._is_ready:
            raise Exception("Qdrant unavailable")
    
    def _ensure_collection_exists(self):
        try:
            self._client.get_collection(self.collection_name)
        except Exception as e:
            self._client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=128, distance=Distance.COSINE),
            )
            print(f"INFO: Collection '{self.collection_name}' created.")

    def search_documents(self, collection_name: str, query_vector: List[float], limit: int):
        """Search dokumen di Qdrant dengan auto-reconnect."""
        self._ensure_ready()
        
        try:
            return self._client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=limit,
            )
        except Exception as e:
            self._is_ready = False
            raise Exception(f"Qdrant unavailable: {e}")
    
    def upsert_document(self, collection_name: str, id: int, vector: List[float], payload: dict):
        """Upsert dokumen ke Qdrant dengan auto-reconnect."""
        self._ensure_ready()
        
        try:
            self._client.upsert(
                collection_name=collection_name,
                points=[PointStruct(id=id, vector=vector, payload=payload)]
            )
        except Exception as e:
            self._is_ready = False
            raise Exception(f"Qdrant unavailable: {e}")
    