from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import models
from db.database import SessionLocal
from db.models import Task as TaskModel


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_task_from_db(task_id: int, db: Session = Depends(get_db)) -> TaskModel:
    task_db = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} does not exist.",
        )
    return task_db
