"""Class for defining a LineString GeoJSON feature"""
from interfaces.feature_abc import FeatureAbstractClass


class LineString(FeatureAbstractClass):
    """Class for defining a LineString GeoJSON feature"""

    def __init__(self, properties: dict = None) -> None:
        super().__init__(properties)
        self.feature_type = "LineString"

    def get_formatted_feature(self) -> dict:
        """Return a GeoJSON LineString"""
        return {
            "type": "Feature",
            "properties": self.properties,
            "geometry": {
                "coordinates": self.coordinates,
                    "type": self.feature_type
            }
        }
