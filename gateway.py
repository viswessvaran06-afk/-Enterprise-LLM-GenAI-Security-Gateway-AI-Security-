from fastapi import APIRouter
from app.models.prompt_model import PromptRequest, PromptResponse
from app.services.llm_proxy import proxy_to_llm

router = APIRouter()

@router.post("/chat", response_model=PromptResponse)
async def chat(request: PromptRequest):
    response = await proxy_to_llm(request)
    return response