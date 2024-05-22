"""Module for describing an Instructions Table"""


class Instruction:
    """Class for describing an Instructions Table"""

    def __init__(self, angle: float, speed: int, distance: float) -> None:
        self.angle = angle
        self.speed = speed
        self.distance = distance

    def __repr__(self) -> str:
        return f"<Instruction(angle={self.angle}, speed={self.speed}, distance={self.distance})"
