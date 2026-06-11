from fastapi import APIRouter, Depends
from app.models.prompt_model import PromptRequest, PromptResponse
from app.services.llm_proxy import proxy_to_llm
from app.services.auth import verify_api_key
from app.services.rate_limiter import check_rate_limit

router = APIRouter()

@router.post("/chat", response_model=PromptResponse)
async def chat(
    request: PromptRequest,
    user_info: dict = Depends(verify_api_key)
):
    check_rate_limit(user_info["user_id"])

    request.user_id = user_info["user_id"]
    request.department = user_info["department"]

    response = await proxy_to_llm(request)
    return response