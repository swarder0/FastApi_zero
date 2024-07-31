from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert response.json()["token_type"] == "bearer"


def test_token_expired_after_time(client, user):
    with freeze_time("2023-07-23 12:00:00"):
        reponse = client.post(
            "/auth/token",
            data={"username": user.email, "password": user.clean_password},
        )
        assert reponse.status_code == HTTPStatus.OK
        token = reponse.json()["access_token"]

    with freeze_time("2023-07-23 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "wronguser",
                "email": "wronguser@example.com",
                "password": "XXXXXXXXXXXXX",
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_token_wrong_username(client, user):
    response = client.post(
        "/auth/token",
        data={"username": "wronguser@example.com", "password": user.clean_password},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_token_wrong_password(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": "wrongpassword"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}
