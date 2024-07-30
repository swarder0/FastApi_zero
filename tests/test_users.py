from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client, token):
    response = client.post(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 2,
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/ {user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "password": "123",
            "username": "testupdate",
            "email": "testupdate@test.com",
            "id": 1,
        },
    )
    assert response.json() == {
        "username": "testupdate",
        "email": "testupdate@test.com",
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
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_found(client, user, token):
    response = client.delete("/users/99", headers={"Authorization": f"Bearer {token}"})
    print(response.json())
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user_wrong_user(client, user_1, token):
    response = client.delete(
        f"/users/{user_1.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


def test_get_a_user_not_found(client, token):
    response = client.get("/users/999", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_get_a_user(client, user, token):
    response = client.get(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "Teste",
        "email": "teste@test.com",
        "id": 1,
    }


def test_post_user_with_same_email(client, user, token):
    response = client.post(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "password": "senha_super_senha",
            "username": "teste2",
            "email": "teste@test.com",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}


def test_post_user_with_same_username(client, user, token):
    response = client.post(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "password": "senha_super_senha",
            "username": "Teste",
            "email": "testename2@example.com",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}


def test_delete_user_with_user_admin(client, user_1, token_admin):
    response = client.delete(
        f"/users/{user_1.id}", headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.status_code == HTTPStatus.OK
