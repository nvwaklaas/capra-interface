"""Abstract class for Route"""
from abc import ABC, abstractmethod


class RouteAbstractClass(ABC):
    """Abstract class for Route"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_formatted_instruction(self) -> dict:
        """Returns a formatted route in JSON format"""
