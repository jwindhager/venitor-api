from datetime import datetime
from pydantic import BaseModel
from typing import List


class Device(BaseModel):
    id: str = None
    date_added: datetime = None
    documents: List[str] = None


class DeviceEvent(BaseModel):
    id: str = None
    device_id: str = None
    device_status: str = None
    device_location: str = None
    device_geolocation: str = None
    device_capacity: int = None
    device_occupancy: int = None
    timestamp: datetime = None
