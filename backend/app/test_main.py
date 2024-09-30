import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)


def generate_conversation():
    with TestClient(app) as client:
        response = client.post(
            "/conversations/",
            headers={"Content-Type": "application/json"},
            json={
                "name": "Initial Chat 1",
                "llm_params": {
                    "model_name": "gpt-3.5-turbo",
                    "temperature": 0.25
                }
            },
        )
        return response

def test_create_conversation():
    response = generate_conversation()

    assert response.status_code == 201
    assert len(response.json()['id']) == 24

def test_get_conversation():
    with TestClient(app) as client:
        response = client.get("/conversations/")
        assert response.status_code == 200

def test_get_conversation_by_id():
    with TestClient(app) as client:
        response = generate_conversation()
        res_id = response.json()['id']
        url = f"/conversations/{res_id}"
        response = client.get(url)
        assert response.status_code == 200

def test_delete_conversation_by_id():
    with TestClient(app) as client:
        response = generate_conversation()
        res_id = response.json()['id']
        url = f"/conversations/{res_id}"
        response = client.delete(url)
        assert response.status_code == 204
