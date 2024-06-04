"""Module containing helper functions for controlling a Capra Hircus Robot"""
import json
import time
import logging
import math
import paho.mqtt.client as mqtt
from geopy.distance import geodesic
from models.driving_instruction import DrivingInstruction
from models.coordinate import Coordinate

# pylint: disable=line-too-long
TOPIC_SEND_PATH = 'capra/navigation/send_path'
TOPIC_REMOTE = "capra/remote/direct_velocity"
TOPIC_SET_MODE = "capra/robot/set_operation_mode"

# Radius of the earth in kilometres
R = 6371.0


class ControlCapra():
    """
    Class for controlling a Capra Hircus using MQTT Protocol
    """

    def __init__(self, broker_address: str, broker_port: int) -> None:
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.logger.setLevel(logging.INFO)

    def connect_to_robot(self) -> None:
        """Establishes connection to Capra Hircus"""
        try:
            self.logger.info("Connecting to robot at %s:%d",
                             self.broker_address, self.broker_port)
            self.client.connect(self.broker_address, self.broker_port)
            self.logger.info("Successfully connected to robot")
        except ConnectionRefusedError:
            self.logger.error("Connection refused")
        except ConnectionAbortedError:
            self.logger.error("Connection aborted")
        except ConnectionResetError:
            self.logger.error("Connection reset")
        except ConnectionError as e:
            self.logger.error(
                "An unexpected error occured during connection: %s", e)

    def mq_set_mode(self, mode: int) -> None:
        """Sets the mode of the Capra Hircus."""
        mode_message = '{"operation_mode": %d}' % (mode)
        try:
            self.client.publish(TOPIC_SET_MODE, mode_message)
            self.logger.info("Mode set to: %d", mode)
        except ConnectionError as e:
            self.logger.error(
                "An unexpected error occured during setting mode: %s", e)

    @staticmethod
    def load_path_file(filename: str) -> dict:
        """Loads a Capra Hircus path file in json format."""
        try:
            with open(filename, encoding="utf-8") as f:
                data = json.load(f)
                logging.info("Path file %s loaded successfully", filename)
        except FileNotFoundError:
            logging.error("The file %s was not found.", filename)
            data = {}
        return data

    def send_path(self, filename: str) -> None:
        """Sends a path to drive structured in the format as specified on the Capra Hircus documentation."""
        msg = self.load_path_file(filename)
        msg_json = json.dumps(msg)
        try:
            self.client.publish(TOPIC_SEND_PATH, msg_json)
            self.logger.info("Path sent from file: %s", filename)
        except ConnectionError as e:
            self.logger.error(
                "An unexpected error occured during sending path: %s", e)

    def calculate_distance_angle(self, coord_1: Coordinate, coord_2: Coordinate) -> dict:
        """Calculates the distance and angle between two coordinates using the Haversine formula."""
        lat1 = math.radians(coord_1[0])
        lon1 = math.radians(coord_1[1])
        lat2 = math.radians(coord_2[0])
        lon2 = math.radians(coord_2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c

        self.logger.info(
            "Calculated distance: %f and angle: %f between coordinates", distance, c)
        return {"distance": distance, "angle": c}

    def calculate_distances_from_path(self, filename: str) -> list:
        """Opens a route file and calculates distance between each node."""
        data = self.load_path_file(filename)
        distances = []
        position = "position"
        nodes = "nodes"

        try:
            for i in range(len(data[nodes])-1):
                x_1 = data[nodes][i][position]["x"]
                y_1 = data[nodes][i][position]["y"]
                coord_1 = (x_1, y_1)
                x_2 = data[nodes][i+1][position]["x"]
                y_2 = data[nodes][i+1][position]["y"]
                coord_2 = (x_2, y_2)
                distances.append(geodesic(coord_1, coord_2).km * 1000)
            self.logger.info("Calculated distances from path: %s", filename)
        except IndexError:
            self.logger.error('Invalid data format in json file: %s', filename)

        return distances

    def send_instruction(self, speed: int, angle: float = 0.0) -> None:
        """Used for remotely controlling Capra Hircus using odometry."""
        instruction = DrivingInstruction(speed, angle)
        msg_json = json.dumps(instruction.get_formatted_instruction())
        try:
            self.client.publish(TOPIC_REMOTE, msg_json)
            self.logger.info("Sent instruction: %s", msg_json)
        except ConnectionError as e:
            self.logger.error(
                "An unexpected error occured during sending instruction: %s", e)

    def remote_control(self, distance: float = 0.1, speed: int = 0, angle: float = 0.0) -> None:
        """Instructs a Capra Hircus robot to drive for a given distance, with a given angle and speed."""
        frequency = 0.1  # 10 Hz
        distance_covered = 0.0

        if speed == 0:
            distance_per_instruction = 0.1
            distance = 0.1
        else:
            distance_per_instruction = abs(speed) * frequency

        while distance_covered < distance:
            self.send_instruction(speed, angle)
            time.sleep(frequency)
            self.logger.info("Distance covered: %f/%f",
                             distance_covered, distance)
            distance_covered += distance_per_instruction
