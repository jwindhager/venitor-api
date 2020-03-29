from fastapi import Depends, FastAPI
from starlette.responses import RedirectResponse
from typing import Dict

import settings

from auth import create_login_redirect_response, request_access_token, get_access_token

app = FastAPI()


@app.get("/")
async def root() -> Dict:
    return {"hello": "world"}


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
