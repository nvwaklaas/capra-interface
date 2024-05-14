"""Pytest testcases for testing the ControlCapra class using MagicMock.
MagicMock is used to be able to test ControlCapra without needing a connection to the robot"""
from unittest.mock import MagicMock
import pytest
from capra_control import ControlCapra

# pylint: disable=line-too-long


@pytest.fixture(name="mqtt_client")
def mock_mqtt_client():
    """Create mock mqtt client"""
    return MagicMock()


@pytest.fixture(name="controller")
def control_capra(mqtt_client):
    """Create instance of ControlCapra Class"""
    capra = ControlCapra("test_broker_address", 1234)
    capra.client = mqtt_client
    return capra


def test_connect_to_robot(controller, mqtt_client):
    """Testing connect_to_robot() method"""
    controller.connect_to_robot()
    mqtt_client.connect.assert_called_once_with(
        "test_broker_address", 1234)


def test_mq_set_mode_stop(controller, mqtt_client):
    """Tests if the Capra Controller can set the mode to 1 (Stopped)"""
    controller.mq_set_mode(1)
    mqtt_client.publish.assert_called_once_with(
        "capra/robot/set_operation_mode", '{"operation_mode": 1}')


def test_mq_set_mode_run(controller, mqtt_client):
    """Tests if the Capra Controller can set the mode to 2 (Running)"""
    controller.mq_set_mode(2)
    mqtt_client.publish.assert_called_once_with(
        "capra/robot/set_operation_mode", '{"operation_mode": 2}')


def test_load_path_file(controller):
    """Tests if a Capra path file can be loaded from disk"""
    path_data = controller.load_path_file("data/Path2.json")
    assert isinstance(path_data, dict)


def test_calculate_distance_angle(controller):
    """Tests if distances and angles are calculated correctly with Haversine"""
    coord_1 = (52.2296756, 21.0122287)  # Warsaw
    coord_2 = (51.5074, 0.1278)         # London
    result = controller.calculate_distance_angle(coord_1, coord_2)

    angle = round(result["angle"], 4)
    distance = round(result["distance"], 4)

    assert isinstance(result, dict)
    assert "distance" in result
    assert "angle" in result
    assert distance == 1431.1784
    assert angle == 0.2246


def test_calculate_distances_from_path(controller):
    """Tests if distances are calculated from Capra Pathfile"""

    distances = controller.calculate_distances_from_path(
        "data/Path2.json")
    assert isinstance(distances, list)


def test_send_instruction(controller, mqtt_client):
    """Tests if an instruction can be send using CapraControl"""
    controller.send_instruction(1, 0.4)
    mqtt_client.publish.assert_called_once_with(
        'capra/remote/direct_velocity',
        '{"header": {"frame_id": "frame_id"}, "twist": {"linear": {"x": 1}, "angular": {"z": 0.4}}}')


def test_remote_control(controller):
    """Tests if CanpraControl can be used to control Capra Hircus remotely"""
    controller.send_instruction = MagicMock()
    controller.remote_control(0.2, 1, 1.2)
    # Distance = 0.2 and distance per iteration = 0.1, so send_instruction should be called twice
    assert controller.send_instruction.call_count == 2
