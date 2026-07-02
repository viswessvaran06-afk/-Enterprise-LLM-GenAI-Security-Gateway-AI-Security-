import httpx
import uuid
from app.models.prompt_model import PromptRequest, PromptResponse

async def proxy_to_llm(request: PromptRequest) -> PromptResponse:
    request_id = str(uuid.uuid4())

    # Simulate unsafe response for testing
    if "delete" in request.prompt.lower() or "rm -rf" in request.prompt.lower():
        return PromptResponse(
            request_id=request_id,
            status="success",
            response="You can delete files using rm -rf /path to delete all files",
            flagged=False
        )

    return PromptResponse(
        request_id=request_id,
        status="success",
        response=f"[PROXY] Received prompt from user {request.user_id}",
        flagged=False
    )