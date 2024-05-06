"""Pytest tests for testing the FastAPI for controlling Capra Hircus"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .main import app, SessionLocal, Instruction


@pytest.fixture(name="client")
def test_client():
    """Creates test client for testing the API"""
    yield TestClient(app)


def test_create_instruction(client):
    """Testing if instrctions are stored correctly"""

    instruction_data = {"angle": 0.5, "speed": 1, "distance": 0.1}
    response = client.post("/drive/", json=instruction_data)
    assert response.status_code == 200
    instruction = response.json()
    assert instruction["angle"] == 0.5
    assert instruction["speed"] == 1
    assert instruction["distance"] == 0.1

    db: Session = SessionLocal()
    db_instruction = db.query(Instruction).filter(
        Instruction.id == instruction["id"]).first()
    assert db_instruction is not None
    assert db_instruction.angle == 0.5
    assert db_instruction.speed == 1
    assert db_instruction.distance == 0.1


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


def test_get_instruction(client):
    """Testing retrieving instructions"""
    db: Session = SessionLocal()
    instruction = Instruction(angle=0.5, speed=1, distance=0.1)
    db.add(instruction)
    db.commit()

    response = client.get("/instructions/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "angle": 0.5,
                               "speed": 1, "distance": 0.1}


def test_upload_json(client):
    """Testing uploading JSOn files"""
    files = {
        "file": ("test.json", b'{"angle": 0.5, "speed": 1, "distance": 0.1}')}
    response = client.post("/upload-json", files=files)
    assert response.status_code == 200
    assert response.json() == {
        "message": "JSON file uploaded and processed successfully"}
