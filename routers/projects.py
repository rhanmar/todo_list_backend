from fastapi import status, HTTPException, Depends, APIRouter
from db.schemas import Project, ProjectCreate, ProjectUpdate

from sqlalchemy.orm import Session
from db import models
from dependencies import get_db


router = APIRouter(
    prefix="/api/projects",
    # tags=["projects"],
)


@router.get("/")
def get_projects_list(title: str | None = None, db: Session = Depends(get_db)) -> dict:
    result = db.query(models.Project).all()
    if title:
        result = db.query(models.Project).filter(models.Project.title.contains(title)).all()
    return result


@router.get("/{project_id}/", response_model=Project)
def get_project_detail_by_id(project_id: int, db: Session = Depends(get_db)) -> Project:
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} does not exist."
        )
    return db_project


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)) -> Project:
    db_project = models.Project(title=project.title, color=project.color)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}/", status_code=status.HTTP_201_CREATED)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> dict:
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} does not exist."
        )
    db.delete(db_project)
    db.commit()
    return {"response": f"Project with id {project_id} was removed"}


@router.put("/{project_id}/", response_model=Project, status_code=status.HTTP_201_CREATED)
def change_project(project_id: int, project_data: ProjectUpdate, db: Session = Depends(get_db)) -> Project:
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} does not exist."
        )
    db_project.title = project_data.title
    if project_data.color is not None:
        db_project.color = project_data.color
    db_project.is_active = project_data.is_active
    db.commit()
    return db_project

