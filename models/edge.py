"""Edge data type"""
from dataclasses import dataclass


@dataclass
class Edge:
    """Class for defining an edge"""

    uuid: str
    start_node_uuid: str
    end_node_uuid: str

    def get_formatted_edge(self) -> dict:
        """Returns an edge in the correct format for Capra Hircus"""

        return {
            "uuid": self.uuid,
            "start_node_uuid": self.start_node_uuid,
            "end_node_uuid": self.end_node_uuid,
            "actions": [
                {
                    "uuid": "drive",
                    "parameters": [
                            {
                                "key": "speed",
                                "type": 2,
                                "value_float32": 1.0
                            }
                    ]
                }
            ]
        }
