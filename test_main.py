"""Pytest tests for testing the FastAPI for controlling Capra Hircus"""
import sqlite3
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(name="db_session")
def session():
    """Create Mock database"""
    connection = sqlite3.connect(':memory:')
    db_session = connection.cursor()
    yield db_session
    connection.close()


@pytest.fixture
def setup_db(db_session):
    """Prepare database for testing"""
    db_session.execute('''CREATE TABLE instructions
                          (angle float, speed int, distance float)''')

    db_session.connection.commit()


@pytest.fixture(name="client")
def test_client():
    """Creates test client for testing the API"""
    yield TestClient(app)


@pytest.mark.usefixtures("setup_db")
def test_create_instruction(client):
    """Tests if instrctuctions can be created"""
    instruction_data = {"angle": 0.5, "speed": 1, "distance": 0.1}
    response = client.post("/drive/", json=instruction_data)
    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.usefixtures("setup_db")
def test_stop_robot(client):
    """Testing if stopping the robot results in the correct message"""
    response = client.post("/stop/")
    assert response.status_code == 200
    assert response.json() == {"message": "Robot stopped"}


@pytest.mark.usefixtures("setup_db")
def test_connection_failed(client):
    """Testing if the correct error message is returned when connection to the robot failed"""
    response = client.get("/connect_to_robot")
    assert response.status_code == 500
    assert response.json() == {'detail': 'Failed to connect to Capra Hircus'}


@pytest.mark.usefixtures("setup_db")
def test_upload_json(client):
    """Testing uploading JSOn files"""
    files = {
        "file": ("test.json", b'{"angle": 0.5, "speed": 1, "distance": 0.1}')}
    response = client.post("/upload-json", files=files)
    assert response.status_code == 200
    assert response.json() == {
        "message": "JSON file uploaded and processed successfully"}
