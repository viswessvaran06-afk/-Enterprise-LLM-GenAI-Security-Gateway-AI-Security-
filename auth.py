from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

VALID_API_KEYS = {
    "user123-key-abc": {"user_id": "user123", "department": "engineering"},
    "user456-key-def": {"user_id": "user456", "department": "finance"},
    "user789-key-ghi": {"user_id": "user789", "department": "hr"},
}

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
    return VALID_API_KEYS[api_key]