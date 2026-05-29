from fastapi import APIRouter, Depends
from api.requests.security_request import SecurityQuestionRequest
from api.dependencies.use_cases import get_ask_security_uc
from application.use_cases.ask_security_question import AskSecurityQuestionUseCase

router = APIRouter()

@router.post("/ask")
async def ask_security_question(
    request: SecurityQuestionRequest,
    use_case: AskSecurityQuestionUseCase = Depends(get_ask_security_uc),
):
    answer = await use_case.execute(request.question, request.session_id)
    return {"answer": answer, "session_id": request.session_id}
