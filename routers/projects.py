from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import models
from db.models import Project as ProjectModel
from db.schemas import Project, ProjectCreate, ProjectUpdate
from dependencies import get_db, get_project_from_db

router = APIRouter(
    prefix="/api/projects",
    # tags=["projects"],
)


@router.get("/")
def get_projects_list(title: str | None = None, db: Session = Depends(get_db)) -> dict:
    result = db.query(models.Project).all()
    if title:
        result = (
            db.query(models.Project).filter(models.Project.title.contains(title)).all()
        )
    return result


@router.get("/{project_id}/", response_model=Project)
def get_project_detail_by_id(
    project_db: ProjectModel = Depends(get_project_from_db),
) -> ProjectModel:
    return project_db


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)) -> Project:
    db_project = models.Project(title=project.title, color=project.color)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}/", status_code=status.HTTP_201_CREATED)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    project_db: ProjectModel = Depends(get_project_from_db),
) -> dict:
    db.delete(project_db)
    db.commit()
    return {"response": f"Project with id {project_id} was removed"}


@router.put(
    "/{project_id}/", response_model=Project, status_code=status.HTTP_201_CREATED
)
def change_project(
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    project_db: ProjectModel = Depends(get_project_from_db),
) -> Project:
    project_db.title = project_data.title
    if project_data.color is not None:
        project_db.color = project_data.color
    project_db.is_active = project_data.is_active
    db.commit()
    return project_db
