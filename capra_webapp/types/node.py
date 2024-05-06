"""Node data type"""
from dataclasses import dataclass


@dataclass
class Node:
    """Class for defining a node"""

    uuid: str
    sequence_number: int
    x: float
    y: float
    z: float = 0.0

    def get_formatted_node(self) -> dict:
        """Returns a node in the corect format for Capra Hircus"""

        return {
            "uuid": self.uuid,
            "sequence_number": self.sequence_number,
            "position": {
                "x": self.x,
                "y": self.y,
                "z": self.z
            }
        }
