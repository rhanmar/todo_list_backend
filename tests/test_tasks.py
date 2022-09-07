import pytest
from fastapi import status

from db.models import Task


@pytest.mark.tasks
def test_tasks_list(
    test_db,
    client,
    db_session,
    task_with_project_factory,
    project_factory,
    url_tasks_list,
):

    project = project_factory()
    db_session.commit()

    tasks = [task_with_project_factory(project=project) for _ in range(3)]
    db_session.commit()

    response = client.get(url_tasks_list)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == len(tasks)
    task_response = response_json[1]
    task_db = db_session.query(Task).filter(Task.id == task_response["id"]).first()
    assert task_response["title"] == task_db.title
    assert task_response["project_id"] == project.id
    assert task_response["description"] == task_db.description


@pytest.mark.tasks
def test_tasks_detail(
    test_db, client, db_session, task_with_project_factory, url_tasks_detail
):

    task = task_with_project_factory()
    db_session.commit()

    response = client.get(url_tasks_detail.format(task.id))
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["id"] == task.id
    assert response_json["title"] == task.title
    assert response_json["description"] == task.description
    assert response_json["project_id"] == task.project_id


@pytest.mark.tasks
def test_tasks_detail_error(test_db, client, db_session, url_tasks_detail):
    response = client.get(url_tasks_detail.format(0))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.tasks
def test_tasks_create(
    test_db, client, db_session, project_factory, url_tasks_list, url_tasks_detail
):

    project = project_factory()
    db_session.commit()

    response = client.post(
        url_tasks_list,
        json={
            "title": "Test task title 1",
            "project_id": project.id,
            "description": "description 1",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert db_session.query(Task).count() == 1

    task_db = db_session.query(Task).all()[0]
    assert task_db.title == "Test task title 1"
    assert task_db.description == "description 1"
    assert task_db.project_id == project.id

    response = client.get(url_tasks_list)
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1

    response = client.get(url_tasks_detail.format(task_db.id))
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == task_db.id
    assert response_json["title"] == task_db.title
    assert response_json["description"] == task_db.description


@pytest.mark.tasks
def test_tasks_delete(test_db, client, db_session, url_tasks_list, url_tasks_detail):

    response = client.post(
        url_tasks_list,
        json={"title": "Test task title 1", "description": "description 1"},
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    response = client.delete(url_tasks_detail.format(response_json["id"]))
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(url_tasks_list)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 0

    assert db_session.query(Task).count() == 0


@pytest.mark.tasks
def test_tasks_delete_error(test_db, client, db_session, url_tasks_detail):
    response = client.delete(url_tasks_detail.format(0))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.tasks
def test_tasks_change(
    test_db, client, db_session, project_factory, url_tasks_list, url_tasks_detail
):
    response = client.post(
        url_tasks_list,
        json={"title": "Test task title 1", "description": "description 1"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    task_db = db_session.query(Task).all()[0]
    assert task_db.project_id is None

    project = project_factory()
    db_session.commit()

    response = client.put(
        url_tasks_detail.format(task_db.id),
        json={"title": "new title", "project_id": project.id},
    )
    assert response.status_code == status.HTTP_201_CREATED
    db_session.refresh(task_db)
    assert task_db.title == "new title"
    assert task_db.project_id == project.id


@pytest.mark.tasks
def test_tasks_change_error(test_db, client, db_session, url_tasks_detail):
    response = client.put(
        url_tasks_detail.format(0),
        json={"title": "new title", "project_id": 0},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
