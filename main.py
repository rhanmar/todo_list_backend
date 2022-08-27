from fastapi import FastAPI, status, HTTPException, Depends
from db.schemas import Project, Task, ProjectCreate, ProjectUpdate, TaskUpdate, TaskCreate  # , Label, Subtask

from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# TODO
# [+] - crud projects
# [+] - crud tasks
#  [+] - create
#  [+] - put
# [?] - validate args in crud
# [+] - model tasks
# [+] - model projects
# [] - tests
#  [+] - projects
#  [+] - tasks
# [+] - fabrics
# [+] - SQLAlchemy (fastapi tutorial)
# [] - new models
# [] - color in Choices
# [] - migrations (Alembic)
# [] - повторяющийся код убрать (список-деталка Проекта/Тасков)  # TODO next 2
# [+] - Project change and delete DB
#       [+] - change
#       [+] - delete
# [] - расширенный лист (таски + проекты)
# [] - black
# [] - isort


# db_projects: list[Project] = [
#     Project(
#         id=1,
#         title="Project 1",
#         color="purple",
#         is_active=True,
#     ),
#     Project(
#         id=2,
#         title="Project 2",
#         color="blue",
#         is_active=False,
#     ),
# ]

# db_labels: list[Label] = [
#     Label(
#         id=1,
#         title="Label 1",
#         color="green",        
#     ),
#     Label(
#         id=1,
#         title="Label 1",
#         color="green",        
#     ),
# ]

# db_tasks: list[Task] = [
#     Task(
#         id=1,
#         title="Task 1",
#         description="Description 1",
#     ),
#     Task(
#         id=2,
#         title="Task 2",
#         description="Description 2",
#         is_checked=True,
#         project=db_projects[0],
#         # labels=[db_labels[0], db_labels[1]]
#     ),
# ]


# db_subtasks: list[Subtask] = [
#     Subtask(
#         id=1,
#         title="Subtask 1",
#         description="Sub Description 1",
#         is_checked=True,
#         task=db_tasks[0],
#     ),
#     Subtask(
#         id=2,
#         title="Subtask 2",
#         description="Sub Description 2",
#         is_checked=True,
#         task=db_tasks[0],
#     ),
# ]


@app.get('/')
def root() -> dict:
    return {"Welcome": "TodoList App FastAPI"}


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PROJECTS


@app.get("/api/projects/")
def get_projects_list(title: str | None = None, db: Session = Depends(get_db)) -> dict:
    result = db.query(models.Project).all()
    if title:
        result = db.query(models.Project).filter(models.Project.title.contains(title)).all()
    return result


@app.get("/api/projects/{project_id}/", response_model=Project)
def get_project_detail_by_id(project_id: int, db: Session = Depends(get_db)) -> Project:
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} does not exist."
        )
    return db_project


@app.post("/api/projects/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)) -> Project:
    db_project = models.Project(title=project.title, color=project.color)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.delete("/api/projects/{project_id}/", status_code=status.HTTP_201_CREATED)
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


@app.put("/api/projects/{project_id}/", response_model=Project, status_code=status.HTTP_201_CREATED)
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


## TASKS

@app.get("/api/tasks/")
def get_tasks_list(db: Session = Depends(get_db)) -> list[Task]:
    return db.query(models.Task).all()


@app.get("/api/tasks/{task_id}/")
def get_task_detail_by_id(task_id: int, db: Session = Depends(get_db)) -> Task:
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} does not exist."
        )
    return db_task


@app.post("/api/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
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


@app.delete("/api/tasks/{task_id}/", status_code=status.HTTP_201_CREATED)
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


@app.put("/api/tasks/{task_id}/", response_model=Task, status_code=status.HTTP_201_CREATED)
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
