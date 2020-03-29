from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class DeviceStatus(Enum):
    ON = "on"
    OFF = "off"
    MAINTENANCE = "maintenance"
    OUT_OF_ORDER = "out_of_order"


class Device(BaseModel):
    id: int = None
    gmn: Optional[str] = None
    qr_code: Optional[str] = None
    documents: List[str] = None


class DeviceEvent(BaseModel):
    id: int = None
    device_id: int = None
    device_status: DeviceStatus = None
    device_location: str = None
    device_geolocation: str = None
    device_capacity: int = None
    device_occupancy: int = None
    timestamp: datetime = None
