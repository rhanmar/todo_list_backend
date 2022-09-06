from fastapi import status, HTTPException, Depends, APIRouter
from db.schemas import Task, TaskUpdate, TaskCreate

from sqlalchemy.orm import Session
from db import models
from dependencies import get_db


router = APIRouter(
    prefix="/api/tasks",
    # tags=["tasks"],
)


@router.get("/")
def get_tasks_list(db: Session = Depends(get_db)) -> list[Task]:
    return db.query(models.Task).all()


@router.get("/{task_id}/")
def get_task_detail_by_id(task_id: int, db: Session = Depends(get_db)) -> Task:
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} does not exist."
        )
    return db_task


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> Task:
    if task.project_id:
        db_project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
        if not db_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {task.project_id} does not exist."
            )
    db_task = models.Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id if task.project_id else None
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}/", status_code=status.HTTP_201_CREATED)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> dict:
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} does not exist."
        )
    db.delete(db_task)
    db.commit()
    return {"response": f"Task with id {task_id} was removed"}


@router.put("/{task_id}/", response_model=Task, status_code=status.HTTP_201_CREATED)
def change_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} does not exist."
        )
    db_task.title = task_data.title
    db_task.is_checked = task_data.is_checked
    if task_data.description is not None:
        db_task.description = task_data.description
    if task_data.project_id is not None and db_task.project_id != task_data.project_id:
        db_project = db.query(models.Project).filter(models.Project.id == task_data.project_id).first()
        if not db_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can't change Task because Project with id {task_data.project_id} does not exist."
            )
        db_task.project_id = task_data.project_id
    db.commit()
    return db_task
