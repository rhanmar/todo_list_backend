from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from db.database import Base
from main import app
from dependencies import get_db
import factory
from db.models import Project, Task


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def url_projects_list():
    return "api/projects/"


@pytest.fixture()
def url_projects_detail():
    return "api/projects/{}/"


@pytest.fixture()
def url_tasks_list():
    return "api/tasks/"


@pytest.fixture()
def url_tasks_detail():
    return "api/tasks/{}/"


@pytest.fixture()
def project_factory(db_session):
    class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):

        title = factory.Faker("sentence")
        color = factory.Faker("word")

        class Meta:
            model = Project
            sqlalchemy_session = db_session

    return ProjectFactory


@pytest.fixture()
def task_with_project_factory(db_session, project_factory):
    class TaskWithProjectFactory(factory.alchemy.SQLAlchemyModelFactory):

        title = factory.Faker("sentence")
        description = factory.Faker("sentence")
        project = factory.SubFactory(project_factory)

        class Meta:
            model = Task
            sqlalchemy_session = db_session

    return TaskWithProjectFactory
