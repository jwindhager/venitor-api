from datetime import datetime
from fastapi import Depends, FastAPI
from sqlalchemy import func
from starlette.responses import RedirectResponse
from typing import Dict

import db
import settings

from auth import create_login_redirect_response, request_access_token, get_access_token, get_user
from model import Device, DeviceEvent

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
    with db.create_session() as db_session:
        db_device = db.Device(date_added=datetime.now())
        db_session.add(db_device)
        # TODO device documents
        db_session.flush()
        device.id = db_device.device_id
    return device


@app.get("/devices/{device_id}", response_model=Device)
async def get_device(device_id: str, user=Depends(get_user)):
    with db.create_session() as db_session:
        db_device = db_session.query(db.Device).filter_by(device_id=device_id).one()
        return Device(
            id=db_device.device_id,
            date_added=db_device.date_added,
            documents=[],  # TODO device documents
        )


@app.post("/devices/{device_id}/events")
async def add_device_event(device_id: str, device_event: DeviceEvent, user=Depends(get_user)):
    with db.create_session() as db_session:
        db_status = db.Status(
            device_id=device_id,
            timestamp_start=device_event.timestamp,
            timestamp_end=None,
            status=device_event.device_status,
            lat=None,  # TODO geolocation
            lng=None,  # TODO geolocation
            usr_lat=None,  # TODO user location
            usr_lng=None,  # TODO user location
            breathe_frequency=None,
            used_capacity=device_event.device_occupancy,
            tot_capacity=device_event.device_capacity,
        )
        db_session.add(db_status)
        db_session.flush()
        device_event.id = db_status.status_id
    return device_event


@app.get("/devices/{device_id}/events/last")
async def get_last_device_event(device_id: str, user=Depends(get_user)):
    with db.create_session() as db_session:
        subquery = db_session.query(func.max(db.Status.timestamp_start)).filter_by(device_id=device_id).subquery()
        db_status = db_session.query(db.Status).filter_by(device_id=device_id, timestamp_start=subquery).one()
        return DeviceEvent(
            id=db_status.status_id,
            device_id=db_status.device_id,
            device_status=db_status.status,
            device_location=None,  # TODO user location
            device_geolocation=None,  # TODO geolocation
            device_capacity=db_status.tot_capacity,
            device_occupancy=db_status.used_capacity,
            timestamp=db_status.timestamp_start,
        )
