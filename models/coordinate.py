"""Class for defining a coordinate"""


class Coordinate:
    """Class for defining a coordinate"""

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def get_coordinate(self) -> list:
        """Returns a formatted coordinate"""
        return [self.x, self.y]
