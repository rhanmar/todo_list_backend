from fastapi import FastAPI, status, HTTPException, Body
from db.models import Project, Task  # , Label, Subtask


app = FastAPI()

# TODO
# [+] - crud projects
# [] - crud tasks
    #  [] - create
    #  [] - put
# [?] - validate args in crus
    # [] - tasks
    # [] - projects
# [] - tests
# [] - SQLAlchemy
# [] - new models


db_projects: list[Project] = [
    Project(
        id=1,
        title="Project 1",
        color="purple",
    ),
    Project(
        id=2,
        title="Project 2",
        color="blue",
    ),
]

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

db_tasks: list[Task] = [
    Task(
        id=1,
        title="Task 1",
        description="Description 1",
    ),
    Task(
        id=2,
        title="Task 2",
        description="Description 2",
        is_checked=True,
        project=db_projects[0],
        # labels=[db_labels[0], db_labels[1]]
    ),
]

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

## PROJECTS

@app.get("/api/projects")
def get_projects_list() -> dict:
    return db_projects

@app.get("/api/projects/{project_id}")
def get_project_detail(project_id: int) -> Project:
    for item in db_projects:
        if item.id == project_id:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Project with id {project_id} does not exist."
    )

@app.post("/api/projects", status_code=status.HTTP_201_CREATED)
def create_project(project: Project) -> dict:
    db_projects.append(project)
    return {"title": project.title}

@app.delete("/api/projects/{project_id}", status_code=status.HTTP_201_CREATED)
def delete_project(project_id: int):
    for item in db_projects:
        if item.id == project_id:
            db_projects.remove(item)
            return {"response": f"Project with id {project_id} was removed"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Project with id {project_id} does not exist."
    )

@app.put("/api/projects/{project_id}", status_code=status.HTTP_201_CREATED)
def change_project(project_id: int, project_data: Project):
    for item in db_projects:
        if item.id == project_id:
            item.title = project_data.title
            item.color = project_data.color
            return {"response": f"Project with id {project_id} was changed"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Project with id {project_id} does not exist."
    )


## TASKS

@app.get("/api/tasks")
def get_tasks_list() -> dict:
    return db_tasks

@app.get("/api/tasks/{task_id}")
def get_task_detail(task_id: int) -> dict:
    for item in db_tasks:
        if item.id == task_id:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_id} does not exist."
    )



@app.post("/api/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task, project_id: int = Body()) -> dict:
    # db_tasks.append(task)
    return {"title": task.title}


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_201_CREATED)
def delete_task(task_id: int):
    for item in db_tasks:
        if item.id == task_id:
            db_tasks.remove(item)
            return {"response": f"Task with id {task_id} was removed"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_id} does not exist."
    )
