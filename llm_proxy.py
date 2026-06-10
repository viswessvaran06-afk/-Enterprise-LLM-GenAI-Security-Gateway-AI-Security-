import httpx
import uuid
from app.models.prompt_model import PromptRequest, PromptResponse

async def proxy_to_llm(request: PromptRequest) -> PromptResponse:
    request_id = str(uuid.uuid4())

    # Placeholder — real LLM call will be added later
    return PromptResponse(
        request_id=request_id,
        status="success",
        response=f"[PROXY] Received prompt from user {request.user_id}",
        flagged=False
    )