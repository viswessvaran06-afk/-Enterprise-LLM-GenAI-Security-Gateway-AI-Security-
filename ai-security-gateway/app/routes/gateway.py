from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.prompt_model import PromptRequest, PromptResponse
from app.services.llm_proxy import proxy_to_llm
from app.services.auth import verify_api_key
from app.services.rate_limiter import check_rate_limit
from app.services.database import get_db
from app.services.logger import log_request

router = APIRouter()

@router.post("/chat", response_model=PromptResponse)
async def chat(
    request: PromptRequest,
    user_info: dict = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    check_rate_limit(user_info["user_id"])

    request.user_id = user_info["user_id"]
    request.department = user_info["department"]

    response = await proxy_to_llm(request)

    log_request(
        db=db,
        user_id=request.user_id,
        department=request.department,
        model=request.model,
        prompt=request.prompt,
        response=response.response,
        flagged=response.flagged,
        reason=response.reason
    )

    return response