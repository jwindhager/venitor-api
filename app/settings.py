import os

APP_BASE_URL = os.environ["APP_BASE_URL"]
ALLOW_ANONYMOUS = bool(os.environ.get("ALLOW_ANONYMOUS", ""))
KEYCLOAK_CLIENT_ID = os.environ["KEYCLOAK_CLIENT_ID"]
KEYCLOAK_SCOPE = os.environ.get("KEYCLOAK_SCOPE", "")
KEYCLOAK_AUTH_URL = os.environ["KEYCLOAK_AUTH_URL"]
KEYCLOAK_TOKEN_URL = os.environ["KEYCLOAK_TOKEN_URL"]
