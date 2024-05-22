"""Pytest tests for testing the FastAPI for controlling Capra Hircus"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app, SessionLocal, Instruction


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
    instruction = Instruction(angle=0.5, speed=1, distance=10)
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


@pytest.mark.parametrize("angle", [
    (-0.9),
    (1.6)
])
def test_angle_validation(client, angle):
    """Boundary value testing for Angle, should be between -0.8 and 1.5"""
    invalid_data = {"angle": angle, "speed": 1, "distance": 10}
    response = client.post("/drive/", json=invalid_data)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                'ctx': {
                    'error': {},
                },
                'input': angle,
                "loc": ["body", "angle"],
                "msg": "Value error, Angle must be between -0.8 and 1.5 radians",
                "type": "value_error",
                'url': 'https://errors.pydantic.dev/2.7/v/value_error',
            }
        ]
    }


@pytest.mark.parametrize("speed", [
    (3),
    (-3)
])
def test_speed_validation(client, speed):
    """Boundary value testing for Speed, should be between -2, and 2"""
    invalid_data = {"angle": 1, "speed": speed, "distance": 10}
    response = client.post("/drive/", json=invalid_data)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                'ctx': {
                    'error': {},
                },
                'input': speed,
                "loc": ["body", "speed"],
                "msg": "Value error, Speed must be between -2 and 2 m/s",
                "type": "value_error",
                'url': 'https://errors.pydantic.dev/2.7/v/value_error',
            }
        ]
    }


@pytest.mark.parametrize("distance", [
    (101),
    (0),
    (0.05),
    (-1)
])
def test_distance_validation(client, distance):
    """Boundary value testing for Distance, should be between 0.1 and 100"""
    invalid_data = {"angle": 0.5, "speed": 1, "distance": distance}
    response = client.post("/drive/", json=invalid_data)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                'ctx': {
                    'error': {},
                },
                'input': distance,
                "loc": ["body", "distance"],
                "msg": "Value error, Distance must be between 0.1 and 100 meter",
                "type": "value_error",
                'url': 'https://errors.pydantic.dev/2.7/v/value_error',
            }
        ]
    }
