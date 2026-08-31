import datetime
from typing import List
from app.models.schemas import FeedbackItem

_feedback_db: List[FeedbackItem] = []

def record_human_feedback(
    recommendation_id: str,
    expert_id: str,
    decision: str,
    reason: str,
    suggested_field_id: str = None
) -> FeedbackItem:
    """
    Logs feedback from orientation counselors/experts on algorithm recommendations.
    Valid decisions: 'accepted', 'modified', 'rejected'.
    """
    if decision not in ["accepted", "modified", "rejected"]:
        raise ValueError("Décision invalide. Doit être 'accepted', 'modified', ou 'rejected'.")

    item = FeedbackItem(
        recommendation_id=recommendation_id,
        expert_id=expert_id,
        decision=decision,
        suggested_field_id=suggested_field_id,
        reason=reason,
        timestamp=datetime.datetime.utcnow().isoformat()
    )
    _feedback_db.append(item)
    return item

def get_all_feedback() -> List[FeedbackItem]:
    return _feedback_db
