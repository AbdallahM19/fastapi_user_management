"""/app_tests.py"""

from app import app

from fastapi.testclient import TestClient


client = TestClient(app)

# def test_


def test_create_user():
    response = client.post(
        "/users/",
        json={
            "username": "testa",
            "email": "testa@example.com",
            "age": 30
        }
    )
    assert response.status_code == 201
    response = client.post(
        "/users/",
        json={
            "username": "testa",
            "email": "testa@example.com",
            "age": 30
        }
    )
    assert response.status_code == 400

def test_update_user():
    response = client.patch(
        "/users/1",
        json={
            "username": "testa",
            "email": "test-aaaaaaaaaaa@example.com",
            "age": 45
        }
    )
    assert response.status_code == 200

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    json_res = response.json()
    assert isinstance(json_res, list)
    if json_res:
        assert isinstance(json_res[0], dict)

def test_get_current_user():
    response = client.get("/users/me")
    assert response.status_code == 200
    json_res = response.json()
    if json_res:
        assert isinstance(json_res, dict)
        assert 'id' in json_res.keys()
        assert json_res.get('username') == "testa"
        assert json_res.get('email') == "test-aaaaaaaaaaa@example.com"
        assert json_res.get('age') == 45
        assert 'session_id' in json_res.keys()

def test_get_user_by_user_id():
    response = client.get("/users/1")
    assert response.status_code == 200

    json_res = response.json()
    if json_res:
        assert isinstance(json_res, dict)
        assert 'age' in json_res.keys()
        assert 'username' in json_res.keys()

def test_delete_user():
    res = client.delete("/users/1")
    if res.status_code == 200:
        assert res.json() == {"ok": True}
    elif res.status_code == 403:
        assert res.json() == {"detail": "Unauthorized"}
    else:
        assert res.json() == {"detail": "User not found"}

def test_delete_all_user():
    res = client.delete("/users/")
    assert res.status_code == 200