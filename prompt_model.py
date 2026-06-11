from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    model: str = "gpt-4"
    prompt: str
    user_id: str
    department: Optional[str] = "general"

class PromptResponse(BaseModel):
    request_id: str
    status: str
    response: Optional[str] = None
    flagged: bool = False
    reason: Optional[str] = None