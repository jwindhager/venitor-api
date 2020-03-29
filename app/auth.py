import json
import jwt
import requests
import settings

from fastapi import HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from jwt import PyJWTError
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import Dict


class User(BaseModel):
    username: str = None
    anonymous: bool = False


def create_login_redirect_response() -> RedirectResponse:
    redirect_response_url_params = [
        f"response_type=code",
        f"client_id={settings.KEYCLOAK_CLIENT_ID}",
        f"redirect_uri={settings.APP_BASE_URL}/auth",
    ]
    if settings.KEYCLOAK_SCOPE:
        redirect_response_url_params.append(f"scope={settings.KEYCLOAK_SCOPE}")
    return RedirectResponse(settings.KEYCLOAK_AUTH_URL + "?" + "&".join(redirect_response_url_params))


def request_access_token(code: str) -> str:
    access_request_parameters = [
        f"grant_type=authorization_code",
        f"code={code}",
        f"redirect_uri={settings.APP_BASE_URL}/auth",
        f"client_id={settings.KEYCLOAK_CLIENT_ID}",
    ]
    access_response = requests.request("POST", settings.KEYCLOAK_TOKEN_URL, data="&".join(access_request_parameters),
                                       headers={"Content-Type": "application/x-www-form-urlencoded"})
    access_response.raise_for_status()
    access_response_content = json.loads(access_response.content)
    return access_response_content.get("access_token")


def get_access_token(request: Request) -> str:
    authorization = request.headers.get("Authorization")
    if not authorization:
        authorization = request.cookies.get("Authorization")
    scheme, access_token = get_authorization_scheme_param(authorization)
    if not access_token or scheme.lower() != "bearer":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return access_token


def get_credentials(request: Request) -> Dict:
    access_token = get_access_token(request)
    try:
        credentials = jwt.decode(access_token, verify=False)  # TODO
    except PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return credentials


def get_user(request: Request) -> User:
    try:
        credentials = get_credentials(request)
        return User(username=credentials.get("sub"))
    except HTTPException:
        if settings.ALLOW_ANONYMOUS:
            return User(username="Anonymous", anonymous=True)
        raise
