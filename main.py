import time
from fastapi import FastAPI, HTTPException
from Schema.QuestionSchema import QuestionRequest
from Schema.DocumentStoreSchema import DocumentRequest
from Controller.WorkflowController import workflowcontroller

app = FastAPI(title="Learning RAG Demo")

@app.post("/ask")
def ask_question(req: QuestionRequest):
    start = time.time()
    try:
        result = workflowcontroller.rag_workflow(req.question)
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add")
def add_document(req: DocumentRequest):
    try:
        result = workflowcontroller.store_document(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
def status():
    return workflowcontroller.get_status()