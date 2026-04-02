from dataclasses import dataclass
import time
@dataclass
class PacketBuilder:
    timestamp: float

    temperature: float
    altitude: float
    latitude: float
    longitude: float

    hazard_map: list