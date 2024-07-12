from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testname",
            "password": "pass",
            "email": "email@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        "username": "testname",
        "email": "email@test.com",
        "id": 1,
    }


def test_read_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "testname",
                "email": "email@test.com",
                "id": 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "password": "123",
            "username": "test2",
            "email": "test@test.com",
            "id": 1,
        },
    )
    assert response.json() == {
        "username": "test2",
        "email": "test@test.com",
        "id": 1,
    }


def test_updade_user_not_found(client):
    response = client.put(
        "/users/999",
        json={
            "password": "123",
            "username": "test2",
            "email": "test@test.com",
            "id": 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_found(client):
    response = client.delete("/users/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_get_a_user_not_found(client):
    response = client.get("/users/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_get_a_user(client):
    client.post(
        "/users/",
        json={
            "password": "123",
            "username": "test2",
            "email": "test@test.com",
        },
    )
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "test2",
        "email": "test@test.com",
        "id": 1,
    }
