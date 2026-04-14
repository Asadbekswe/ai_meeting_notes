from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import ActionItem
from app.schemas.action_item import ActionItemOut, ActionItemUpdate

router = APIRouter()


@router.get("", response_model=list[ActionItemOut])
def list_action_items(
    status: str | None = Query(default=None),
    owner: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(ActionItem)
    if status:
        query = query.filter(ActionItem.status == status)
    if owner:
        query = query.filter(ActionItem.owner_name_raw == owner)
    return query.order_by(ActionItem.updated_at.desc()).all()


@router.patch("/{action_item_id}", response_model=ActionItemOut)
def update_action_item(action_item_id: UUID, payload: ActionItemUpdate, db: Session = Depends(get_db)):
    item = db.query(ActionItem).filter(ActionItem.id == action_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item
