"""Route Class in GeoSJON format"""

from interfaces.route_abc import RouteAbstractClass


class GeoJSONRoute(RouteAbstractClass):
    """Class for defining a route in GeoJSON format"""

    def __init__(self) -> None:
        self.features = []

    def add_feature(self, feature) -> None:
        """Add GeoJSON feature to Route"""
        self.features.append(feature)
