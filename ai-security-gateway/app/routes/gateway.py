from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.prompt_model import PromptRequest, PromptResponse
from app.services.llm_proxy import proxy_to_llm
from app.services.auth import verify_api_key
from app.services.rate_limiter import check_rate_limit
from app.services.database import get_db
from app.services.logger import log_request
from app.services.pii_detector import anonymize_text

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

    # Scan prompt for PII
    clean_prompt, pii_found, entities = anonymize_text(request.prompt)

    if pii_found:
        log_request(
            db=db,
            user_id=request.user_id,
            department=request.department,
            model=request.model,
            prompt=request.prompt,
            response=None,
            flagged=True,
            reason=f"PII detected: {entities}"
        )
        return PromptResponse(
            request_id="blocked",
            status="blocked",
            response=None,
            flagged=True,
            reason=f"PII detected and removed: {entities}"
        )

    # No PII found, proceed normally
    request.prompt = clean_prompt
    response = await proxy_to_llm(request)

    log_request(
        db=db,
        user_id=request.user_id,
        department=request.department,
        model=request.model,
        prompt=request.prompt,
        response=response.response,
        flagged=False,
        reason=None
    )

    return response