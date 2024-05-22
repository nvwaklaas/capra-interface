"""Module used for defining a DrivingInstruction"""
from interfaces.instruction_abc import InstructionAbstractClass


class DrivingInstruction(InstructionAbstractClass):
    """Class for defining a DrivingInstruction"""

    def __init__(self, speed: int, angle: float):
        self.angle = angle
        self.speed = speed

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
