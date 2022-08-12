from pydantic import BaseModel



class Project(BaseModel):
    id: int | None
    title: str
    color: str | None = None


# class Label(BaseModel):
#     id: int | None
#     title: str
#     color: str


class Task(BaseModel):
    id: int | None
    title: str
    description: str
    project: Project = None
    # labels: list[Label] = None
    is_checked: bool = False
    deadline: str | None = None  # TODO datetime


# class Subtask(BaseModel):
#     id: int | None
#     title: str
#     description: str
#     task: Task
#     is_checked: bool = False
#     labels: list[Label] = None
#     deadline: str | None = None  # TODO datetime
