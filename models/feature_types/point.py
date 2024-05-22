"""Class for defining a Point GeoJSON feature"""
from interfaces.feature_abc import FeatureAbstractClass


class Point(FeatureAbstractClass):
    """Class for defining a Point GeoJSON feature"""

    def __init__(self, properties: dict = None) -> None:
        super().__init__(properties)
        self.feature_type = "Point"

    def get_formatted_feature(self) -> dict:
        """Return a GeoJSON Point"""
        return {
            "type": "Feature",
            "properties": self.properties,
            "geometry": {
                "coordinates": self.coordinates,
                "type": self.feature_type
            }
        }
