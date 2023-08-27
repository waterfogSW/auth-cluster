import time

from fastapi import FastAPI
from jose import jwt
from jose.utils import base64url_encode
from pydantic import BaseModel

import key_util

app = FastAPI()


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(request: LoginRequest):
    payload = {
        "username": request.username,
        "iss": "fastapi-jwks",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600  # Valid for 1 hour
    }
    token = jwt.encode(payload, key_util.private_key_str, algorithm="RS256")
    return {"access_token": token}


@app.get("/decode")
async def decode(token: str):
    return jwt.decode(token, key_util.public_key_str, algorithms=["RS256"])


@app.get("/.well-known/jwks.json")
async def jwks():
    numbers = key_util.public_key.public_numbers()
    n = base64url_encode(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, 'big')).decode()
    e = base64url_encode(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, 'big')).decode()
    jwk = {
        "alg": "RS256",
        "kty": "RSA",
        "use": "sig",
        "n": n,
        "e": e,
        "kid": "abc123"
    }
    return dict(keys=[jwk])
