from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Users with roles and allowed models
VALID_API_KEYS = {
    "user123-key-abc": {
        "user_id": "user123",
        "department": "engineering",
        "role": "admin",
        "allowed_models": ["gpt-4", "gpt-3.5-turbo", "claude-3"]
    },
    "user456-key-def": {
        "user_id": "user456",
        "department": "finance",
        "role": "analyst",
        "allowed_models": ["gpt-3.5-turbo"]
    },
    "user789-key-ghi": {
        "user_id": "user789",
        "department": "hr",
        "role": "basic",
        "allowed_models": ["gpt-3.5-turbo"]
    },
}

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
    return VALID_API_KEYS[api_key]

def check_model_access(user_info: dict, requested_model: str):
    allowed_models = user_info.get("allowed_models", [])
    if requested_model not in allowed_models:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"Your role '{user_info['role']}' does not have access to model '{requested_model}'. Allowed models: {allowed_models}"
        )