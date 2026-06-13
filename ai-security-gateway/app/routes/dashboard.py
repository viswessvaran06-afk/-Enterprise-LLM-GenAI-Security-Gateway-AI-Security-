from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.services.database import get_db
from app.models.audit_log import AuditLog

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    # Total requests
    total_requests = db.query(AuditLog).count()

    # Total flagged requests
    total_flagged = db.query(AuditLog).filter(AuditLog.flagged == True).count()

    # Total blocked (no response)
    total_blocked = db.query(AuditLog).filter(
        AuditLog.flagged == True,
        AuditLog.response == None
    ).count()

    # Requests by department
    by_department = db.query(
        AuditLog.department,
        func.count(AuditLog.id).label("count")
    ).group_by(AuditLog.department).all()

    # Recent flagged requests
    recent_flagged = db.query(AuditLog).filter(
        AuditLog.flagged == True
    ).order_by(AuditLog.timestamp.desc()).limit(5).all()

    return {
        "total_requests": total_requests,
        "total_flagged": total_flagged,
        "total_blocked": total_blocked,
        "by_department": [
            {"department": d, "count": c} for d, c in by_department
        ],
        "recent_flagged": [
            {
                "user_id": log.user_id,
                "department": log.department,
                "prompt": log.prompt[:50] + "...",
                "reason": log.reason,
                "timestamp": str(log.timestamp)
            }
            for log in recent_flagged
        ]
    }