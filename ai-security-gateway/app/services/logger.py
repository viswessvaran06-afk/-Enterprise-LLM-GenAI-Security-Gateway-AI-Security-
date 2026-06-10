from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

def log_request(
    db: Session,
    user_id: str,
    department: str,
    model: str,
    prompt: str,
    response: str,
    flagged: bool = False,
    reason: str = None
):
    log = AuditLog(
        user_id=user_id,
        department=department,
        model=model,
        prompt=prompt,
        response=response,
        flagged=flagged,
        reason=reason
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log