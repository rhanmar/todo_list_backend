import pytest
from fastapi import status

from db.models import Project


@pytest.mark.projects
def test_projects_list(test_db, client, db_session, project_factory, url_projects_list):

    projects = [project_factory() for _ in range(5)]
    db_session.commit()

    response = client.get(url_projects_list)
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == len(projects)


@pytest.mark.projects
def test_project_detail(
    test_db, client, db_session, project_factory, url_projects_detail
):

    item = project_factory()
    db_session.commit()

    response = client.get(url_projects_detail.format(item.id))
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == item.id
    assert response_json["title"] == item.title
    assert response_json["color"] == item.color


# https://stackoverflow.com/questions/67255653/how-to-set-up-and-tear-down-a-database-between-tests-in-fastapi
# https://dev.to/jbrocher/fastapi-testing-a-database-5ao5


@pytest.mark.projects
def test_project_detail_error(test_db, client, db_session, url_projects_detail):
    response = client.get(url_projects_detail.format(0))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.projects
def test_create_project(
    test_db, client, db_session, url_projects_list, url_projects_detail
):

    response = client.post(
        url_projects_list,
        json={"title": "Test title", "color": "blue", "is_active": False},
    )
    assert response.status_code == 201
    assert len(db_session.query(Project).all()) == 1

    item = db_session.query(Project).all()[0]
    assert item.title == "Test title"
    assert item.color == "blue"

    response = client.get(url_projects_list)
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1

    response = client.get(url_projects_detail.format(item.id))
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == item.id
    assert response_json["title"] == item.title
    assert response_json["color"] == item.color


@pytest.mark.projects
def test_delete_project(
    test_db, client, db_session, url_projects_list, url_projects_detail
):

    response = client.post(
        url_projects_list,
        json={"title": "Test title", "color": "blue", "is_active": False},
    )
    assert response.status_code == 201

    items = db_session.query(Project).all()
    assert len(items) == 1

    response_json = response.json()
    response = client.delete(url_projects_detail.format(response_json["id"]))
    assert response.status_code == 201

    response = client.get(url_projects_list)
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 0

    items = db_session.query(Project).all()
    assert len(items) == 0


@pytest.mark.projects
def test_delete_project_error(
    test_db, client, db_session, url_projects_list, url_projects_detail
):
    response = client.delete(url_projects_detail.format(0))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.projects
def test_change_project(
    test_db, client, db_session, url_projects_list, url_projects_detail
):

    response = client.post(
        url_projects_list,
        json={"title": "Test title", "color": "blue", "is_active": False},
    )
    assert response.status_code == 201
    assert len(db_session.query(Project).all()) == 1

    item = db_session.query(Project).all()[0]
    response = client.put(
        url_projects_detail.format(item.id),
        json={"title": "Brand new title", "is_active": True},
    )
    assert response.status_code == 201
    db_session.refresh(item)
    assert item.title == "Brand new title"
    assert item.is_active is True
    assert item.color == "blue"


@pytest.mark.projects
def test_change_project_error(
    test_db, client, db_session, url_projects_list, url_projects_detail
):
    response = client.put(
        url_projects_detail.format(0),
        json={"title": "Brand new title", "is_active": True},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
