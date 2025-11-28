from pydantic import BaseModel

class DocumentRequest(BaseModel):
    text: str