"""Abstract class for GeoJSON feature"""
from abc import ABC, abstractmethod
from models.coordinate import Coordinate


class FeatureAbstractClass(ABC):
    """Abstract class for GeoJSON feature"""

    @abstractmethod
    def __init__(self, properties: dict = None) -> None:
        self.coordinates = []
        self.properties = properties

    def add_coordinate(self, coordinate: Coordinate) -> None:
        """Add coordinate to Feature"""
        self.coordinates.append(coordinate)

    @abstractmethod
    def get_formatted_feature(self) -> dict:
        """Returns a GeoJSON feature"""
