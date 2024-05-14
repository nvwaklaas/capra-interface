"""Module used for defining a DrivingInstruction"""
from dataclasses import dataclass


@dataclass
class DrivingInstruction:
    """Class for defining a DrivingInstruction"""

    speed: int
    angle: float = 0.0

    def get_formatted_instruction(self):
        """Returns a driving instruction in the correct format for Capra Hircus"""

        return {
            "header": {
                "frame_id": "frame_id"
            },
            "twist": {
                "linear": {
                    "x": self.speed
                },
                "angular": {
                    "z": self.angle
                }
            }
        }
