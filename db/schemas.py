from pydantic import BaseModel


# BASE Project
class ProjectBase(BaseModel):
    title: str
    color: str | None = None
    is_active: bool = True


# CREATE Project
class ProjectCreate(ProjectBase):
    pass


# UPDATE Project
class ProjectUpdate(ProjectBase):
    pass


# READ Project
class Project(ProjectBase):
    id: int | None

    class Config:
        orm_mode = True


############


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    # labels: list[Label] = None
    # deadline: str | None = None  # TODO datetime


class TaskCreate(TaskBase):
    project_id: int | None


class TaskUpdate(TaskBase):
    is_checked: bool = False
    project_id: int | None


class Task(TaskBase):
    id: int | None
    project: Project = None
    is_checked: bool = False

    class Config:
        orm_mode = True


# class Subtask(BaseModel):
#     id: int | None
#     title: str
#     description: str
#     task: Task
#     is_checked: bool = False
#     labels: list[Label] = None
#     deadline: str | None = None  # TODO datetime

# class Label(BaseModel):
#     id: int | None
#     title: str
#     color: str
