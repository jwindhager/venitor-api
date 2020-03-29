from datetime import datetime
from fastapi import Depends, FastAPI
from starlette.responses import RedirectResponse
from typing import Dict

import settings

from auth import create_login_redirect_response, request_access_token, get_access_token, get_user
from model import Device, DeviceStatus, DeviceEvent

app = FastAPI()


@app.get("/login")
async def login() -> RedirectResponse:
    return create_login_redirect_response()


@app.get("/auth")
async def auth(code: str) -> RedirectResponse:
    access_token = request_access_token(code)
    redirect_response = RedirectResponse(settings.APP_BASE_URL)
    redirect_response.set_cookie("Authorization", value=f"Bearer {access_token}")
    return redirect_response


@app.get("/token")
async def token(access_token: str = Depends(get_access_token)) -> Dict:
    return {"access_token": access_token}


@app.post("/devices")
async def add_device(device: Device, user=Depends(get_user)):
    device.id = 123
    return device


@app.get("/devices/{device_id}", response_model=Device)
async def get_device(device_id: int, user=Depends(get_user)):
    return Device(
        id=device_id,
        gmn="TODO GMN format",
        readonly_qr="TODO QR code format",
        readwrite_qr="TODO QR code format",
        documents=["http://www.example.com"],
    )


@app.get("/devices/by_gmn/{gmn}", response_model=Device)
async def get_device(gmn: str, user=Depends(get_user)):
    return Device(
        id=123,
        gmn=gmn,
        qr_code="TODO QR code format",
        documents=["http://www.example.com"],
    )


@app.get("/devices/by_qr_code/{qr_code}", response_model=Device)
async def get_device(qr_code: str, user=Depends(get_user)):
    return Device(
        id=123,
        gmn="TODO GMN format",
        qr_code=qr_code,
        documents=["http://www.example.com"],
    )


@app.post("/devices/{device_id}/events")
async def add_device_event(device_id: str, device_event: DeviceEvent, user=Depends(get_user)):
    device_event.id = 123
    device_event.device_id = device_id
    device_event.timestamp = datetime.now()
    return device_event


@app.get("/devices/{device_id}/events/last")
async def get_last_device_event(device_id: str, user=Depends(get_user)):
    return DeviceEvent(
        id=123,
        device_id=device_id,
        device_status=DeviceStatus.ON,
        device_location="TODO Location format",
        device_geolocation="TODO Location format",
        device_capacity=1,
        device_occupancy=0,
        timestamp=datetime.today(),
    )
