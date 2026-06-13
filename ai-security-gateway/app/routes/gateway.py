from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.prompt_model import PromptRequest, PromptResponse
from app.services.llm_proxy import proxy_to_llm
from app.services.auth import verify_api_key
from app.services.rate_limiter import check_rate_limit
from app.services.database import get_db
from app.services.logger import log_request
from app.services.pii_detector import anonymize_text
from app.services.injection_detector import detect_injection
from app.services.content_filter import filter_response

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

    # Check for prompt injection
    is_injection, pattern = detect_injection(request.prompt)
    if is_injection:
        log_request(
            db=db,
            user_id=request.user_id,
            department=request.department,
            model=request.model,
            prompt=request.prompt,
            response=None,
            flagged=True,
            reason=f"Prompt injection detected: {pattern}"
        )
        return PromptResponse(
            request_id="blocked",
            status="blocked",
            response=None,
            flagged=True,
            reason="Prompt injection attack detected and blocked"
        )

    # Anonymize PII in prompt
    clean_prompt, pii_found, entities = anonymize_text(request.prompt)
    original_prompt = request.prompt
    request.prompt = clean_prompt

    # Send anonymized prompt to LLM
    response = await proxy_to_llm(request)

    # Filter response for unsafe content
    safe_response, is_unsafe, unsafe_pattern = filter_response(response.response)
    if is_unsafe:
        log_request(
            db=db,
            user_id=request.user_id,
            department=request.department,
            model=request.model,
            prompt=original_prompt,
            response=None,
            flagged=True,
            reason=f"Unsafe response blocked: {unsafe_pattern}"
        )
        return PromptResponse(
            request_id="blocked",
            status="blocked",
            response=None,
            flagged=True,
            reason=f"Response violated corporate policy and was blocked"
        )

    # Log request
    log_request(
        db=db,
        user_id=request.user_id,
        department=request.department,
        model=request.model,
        prompt=original_prompt,
        response=safe_response,
        flagged=pii_found,
        reason=f"PII anonymized: {entities}" if pii_found else None
    )

    if pii_found:
        response.flagged = True
        response.reason = f"PII detected and anonymized: {entities}"

    return response