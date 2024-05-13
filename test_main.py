"""Pytest tests for testing the FastAPI for controlling Capra Hircus"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(name="client")
def test_client():
    """Creates test client for testing the API"""
    yield TestClient(app)


def test_create_instruction(client):
    """Tests if instrctuctions can be created"""
    instruction_data = {"angle": 0.5, "speed": 1, "distance": 0.1}
    response = client.post("/drive/", json=instruction_data)
    assert response.status_code == 200
    assert "id" in response.json()


def test_stop_robot(client):
    """Testing if stopping the robot results in the correct message"""
    response = client.post("/stop/")
    assert response.status_code == 200
    assert response.json() == {"message": "Robot stopped"}


def test_connection_failed(client):
    """Testing if the correct error message is returned when connection to the robot failed"""
    response = client.get("/connect_to_robot")
    assert response.status_code == 500
    assert response.json() == {'detail': 'Failed to connect to Capra Hircus'}


def test_upload_json(client):
    """Testing uploading JSOn files"""
    files = {
        "file": ("test.json", b'{"angle": 0.5, "speed": 1, "distance": 0.1}')}
    response = client.post("/upload-json", files=files)
    assert response.status_code == 200
    assert response.json() == {
        "message": "JSON file uploaded and processed successfully"}
