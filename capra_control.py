"""Module containing helper functions for controlling a Capra Hircus Robot"""
import json
import time
import logging
import math
import paho.mqtt.client as mqtt
from geopy.distance import geodesic
from models.driving_instruction import DrivingInstruction

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
        logging.basicConfig()
        self.logger.setLevel(logging.INFO)

    def connect_to_robot(self) -> None:
        """Establishes connection to Capra Hircus"""
        try:
            self.client.connect(self.broker_address, self.broker_port)
        except ConnectionRefusedError:
            print('Connection refused')
        except ConnectionAbortedError:
            print('Connection aborted')
        except ConnectionResetError:
            print('Connection reset')
        except ConnectionError as e:
            print(f"An unexpected error occured during connection: {e}")

    def mq_set_mode(self, mode: int) -> None:
        """Sets the mode of the Capra Hircus.  
        Available modes are:\n
        STOPPED=1\n
        RUNNING=2\n
        ABORTING=3\n
        ABORTED=4\n
        PAUSED=5

        Modes are used to send different types of instructions to the robot.
        """

        mode = '{"operation_mode": %d}' % (mode)
        try:
            self.client.publish(TOPIC_SET_MODE, mode)
            self.logger.info("\nMode set to: %s", mode)
        except ConnectionError as e:
            self.logger.error(
                "An unexpected error occured during connection: %s.", e)

    @staticmethod
    def load_path_file(filename: str) -> dict:
        """
        load_path_file() loads a Capra Hircus path file in json format.
        A Capra Hircus path file can be created using the Capra Commander Mobile application.
        This mobile application can be found on the official Capra Hircus documentation
        """

        try:
            with open(filename, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("The file {filename} was not found.")

        return data

    def send_path(self, filename: str) -> None:
        """Sends a path to drive structured in the format as specified on the Capra Hircus documentation"""

        # Create message to publish to the topic.
        msg = self.load_path_file(filename)

        msg_json = json.dumps(msg)
        try:
            self.client.publish(TOPIC_SEND_PATH, msg_json)
            self.logger.info('Path sent')
        except ConnectionError as e:
            self.logger.info(
                "An unexpected error occured during connection: %s.", e)

    def calculate_distance_angle(self, coord_1, coord_2) -> dict:
        """Calculates the distance and angle between two coordinates using the Haversine formula"""

        # Convert degrees to radians
        lat1 = math.radians(coord_1[0])
        lon1 = math.radians(coord_1[1])
        lat2 = math.radians(coord_2[0])
        lon2 = math.radians(coord_2[1])

        # Difference in longitudes and latitudes
        dlon = lon2 - lon1
        print(f"dlon: {dlon}")
        dlat = lat2 - lat1
        print(f"dlate: {dlat}")

        # Haversine formula
        a = math.sin(dlat/2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlon/2)**2

        # Calculating angle between coorindates
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        # Calculate the distance
        distance = R * c

        return {"distance": distance, "angle": c}

    def calculate_distances_from_path(self, filename: str) -> list:
        """Opens a route file and calculates distance between each node.\n
        Input file should be a json file in the format that is used by
        a Capra Hircus robot"""

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

                # using geopy to calculate distance between coordinates in metres.
                distances.append(geodesic(coord_1, coord_2).km * 1000)
        except IndexError:
            self.logger.error('Invalid data format in json file.')

        return distances

    def send_instruction(self, speed, angle: float = 0.0) -> None:
        """Used for remotely controlling Capra Hircus using odometry."""

        instruction = DrivingInstruction(speed, angle)

        # Get instruction string as specified by Capra documentation
        msg_json = json.dumps(instruction.get_formatted_instruction())

        try:
            self.client.publish(TOPIC_REMOTE, msg_json)
        except ConnectionError as e:
            self.logger.error(
                "An unexpected error occured during connection: %s.", e)

    def remote_control(self, distance: float = 0.1, speed: int = 0, angle=0.0) -> None:
        """Instructs a Capra Hircus robot to drive for a given distance, with a given angle and speed."""

        frequency = 0.1  # 10 Hz
        distance_covered = 0.0

        if speed == 0:
            # set distance to prevent endless loop.
            distance_per_instruction = 0.1
            distance = 0.1
        else:
            # Use absolute value as speed can be negative
            distance_per_instruction = abs(speed) * frequency

        # Sends instructions to drive until distance is fully covered.
        while distance_covered < distance:
            self.send_instruction(speed, angle)
            # Pausing in order to send instructions at 10 Hz.
            time.sleep(frequency)
            self.logger.info("Distance covered: %f/%f",
                             distance_covered, distance)
            distance_covered += distance_per_instruction
