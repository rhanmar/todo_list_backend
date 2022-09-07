from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import models
from db.database import SessionLocal
from db.models import Project as Project
from db.models import Task as Task


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_task_from_db(task_id: int, db: Session = Depends(get_db)) -> Task:
    task_db = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} does not exist.",
        )
    return task_db


def get_project_from_db(project_id: int, db: Session = Depends(get_db)) -> Project:
    project_db = (
        db.query(models.Project).filter(models.Project.id == project_id).first()
    )
    if not project_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} does not exist.",
        )
    return project_db
