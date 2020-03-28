from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from . import settings

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(settings.OAUTH2_TOKEN_URL)


@app.get("/")
def read_root(token: str = Depends(oauth2_scheme)):
    return {"token": token}
