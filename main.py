import time
from fastapi import FastAPI, HTTPException
from Schema.QuestionSchema import QuestionRequest
from Schema.DocumentStoreSchema import DocumentRequest
from Controller.WorkflowController import workflowcontroller

app = FastAPI(title="Learning RAG Demo")

@app.post("/ask")
def ask_question(req: QuestionRequest):
    try:
        result = workflowcontroller.rag_workflow(req.question)
        return result
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