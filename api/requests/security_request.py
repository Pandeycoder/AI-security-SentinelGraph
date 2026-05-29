from pydantic import BaseModel
import uuid

class SecurityQuestionRequest(BaseModel):
    question: str
    session_id: str = str(uuid.uuid4())
