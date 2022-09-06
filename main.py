from fastapi import FastAPI

from db import models
from db.database import engine
from routers.projects import router as router_projects
from routers.tasks import router as router_tasks

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_projects)
app.include_router(router_tasks)


@app.get("/")
def root() -> dict:
    return {"Welcome": "TodoList App FastAPI"}
