"""Abstract class for Instruction"""
from abc import ABC, abstractmethod


class InstructionABC(ABC):
    """Abstract class for Instruction"""

    @abstractmethod
    def __init__(self, speed: int, angle: float):
        self.speed = speed
        self.angle = angle

    @abstractmethod
    def get_formatted_instruction(self) -> str | dict:
        """Returns a driving instruction str|dict"""
