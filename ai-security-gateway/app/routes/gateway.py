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

    # Anonymize PII in prompt
    clean_prompt, pii_found, entities = anonymize_text(request.prompt)

    # Replace prompt with anonymized version
    original_prompt = request.prompt
    request.prompt = clean_prompt

    # Send anonymized prompt to LLM
    response = await proxy_to_llm(request)

    # Log with original prompt and flag if PII was found
    log_request(
        db=db,
        user_id=request.user_id,
        department=request.department,
        model=request.model,
        prompt=original_prompt,
        response=response.response,
        flagged=pii_found,
        reason=f"PII anonymized: {entities}" if pii_found else None
    )

    if pii_found:
        response.flagged = True
        response.reason = f"PII detected and anonymized: {entities}"

    return response