import os
import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

SUPABASE_JWT_SECRET = os.environ["SUPABASE_JWT_SECRET"]
SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"

bearer_scheme = HTTPBearer(auto_error=False)
_jwks_client = PyJWKClient(JWKS_URL, cache_keys=True, lifespan=3600)


class CurrentUser:
    def __init__(self, user_id: uuid.UUID, email: str | None):
        self.id = user_id
        self.email = email


def _decode_token(token: str) -> dict:
    header = jwt.get_unverified_header(token)
    alg = header.get("alg", "HS256")
    if alg == "HS256":
        return jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
    signing_key = _jwks_client.get_signing_key_from_jwt(token).key
    return jwt.decode(
        token,
        signing_key,
        algorithms=[alg],
        audience="authenticated",
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yetkilendirme gerekli.",
        )
    try:
        payload = _decode_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Geçersiz token: {exc}",
        ) from exc

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token içinde kullanıcı bilgisi yok.",
        )
    return CurrentUser(user_id=uuid.UUID(sub), email=payload.get("email"))
