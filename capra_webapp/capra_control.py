"""Module containing helper functions for controlling a Capra Hircus Robot"""
import json
import time
import paho.mqtt.client as mqtt
from geopy.distance import geodesic
from capra_webapp.types.driving_instruction import DrivingInstruction

TOPIC_SEND_PATH = 'capra/navigation/send_path'
TOPIC_REMOTE = "capra/remote/direct_velocity"
TOPIC_SET_MODE = "capra/robot/set_operation_mode"


class ControlCapra():
    """Class for controlling a Capra Hircus"""

    def __init__(self, broker_address: str, broker_port: int) -> None:
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
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
        """

        mode = '{"operation_mode": %d}' % (mode)
        try:
            self.client.publish(TOPIC_SET_MODE, mode)
            print('\nMode set')
        except ConnectionError as e:
            print(f"An unexpected error occured during connection: {e}.")

    @staticmethod
    def load_path_file(filename: str) -> dict:
        """load_path_file() loads a Capra Hircus path file in json format."""

        try:
            with open(filename, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"The file {filename} was not found.")

        return data

    def send_path(self, filename: str) -> None:
        """Creates a path for the Capra Hircus to drive."""

        msg = self.load_path_file(filename)

        msg_json = json.dumps(msg)
        try:
            self.client.publish(TOPIC_SEND_PATH, msg_json)
            print('\nPath sent')
        except ConnectionError as e:
            print(f"An unexpected error occured during connection: {e}.")

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
                distances.append(geodesic(coord_1, coord_2).km * 1000)
        except IndexError:
            print('Invalid data format in json file.')

    def send_instruction(self, angle: float = 0.0) -> None:
        """Used for remotely controlling Capra Hircus."""

        instruction = DrivingInstruction(angle)
        msg_json = json.dumps(instruction.get_formatted_instruction())

        try:
            self.client.publish(TOPIC_REMOTE, msg_json)
        except ConnectionError as e:
            print(f"An unexpected error occured during connection: {e}.")

    def remote_control(self, distance: float, speed: int, angle=0.0):
        """Instructs a Capra Hircus robot to drive for a given distance."""

        frequency = 0.1  # 10 Hz
        distance_covered = 0.0
        distance_per_instruction = speed * frequency

        # Sends instructions to drive until distance is fully covered.
        while distance_covered < distance:
            self.send_instruction(angle)
            # Pausing in order to send instructions at 10 Hz.
            time.sleep(frequency)
            distance_covered += distance_per_instruction
