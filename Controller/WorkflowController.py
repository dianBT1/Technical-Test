import time
from Services.QdrantClientServices import QdrantClientService
from Services.EmbeddingServices import EmbeddingServices
from Services.DocumentStore import DocumentStore
from Services.RagServices import RagService
from langgraph.graph import StateGraph, END
class WorkflowController:
    def __init__(self):
        self.qdrant_client = QdrantClientService()
        self.embedding_service = EmbeddingServices()
        self.document_store = DocumentStore(self.qdrant_client, self.embedding_service)
        self.rag_service = RagService(self.document_store)
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self.rag_service.simple_retrieve)
        workflow.add_node("answer", self.rag_service.simple_answer)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        chain = workflow.compile()
        return chain

    def rag_workflow(self, question: str):
        start = time.time()
        try:
            result = self.workflow.invoke({"question": question})
            return {
                "question": question,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3)
            }
        except Exception as e:
            raise Exception(f"Error in rag_workflow: {e}")
        

    def store_document(self, text: str):
        return self.document_store.add_document_store(text)

    def get_status(self):
        return {
            "qdrant_ready": self.qdrant_client.is_available(),
            "in_memory_docs_count": self.document_store.in_memory_count,
            "graph_ready": self.workflow is not None
        }

workflowcontroller = WorkflowController()