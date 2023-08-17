import time

from fastapi import FastAPI
from jose import jwt, jwk
from pydantic import BaseModel

app = FastAPI()

key = jwk.construct({
    "p": "74XTFmbRtphGpLzckZ4EWLBg9U7cHlLVu6lekJ8DMIVK9QAYX7FE6K6DHS0EF2-vBzamQ1nCvRPjCwpbHLPGLMk1NC65yVIKeDmy6fMDWlBnzEPgAvtU7IGbrkEhJOudATv6AjbcVhF82lMWkpE813Ikr-wRsP_hUVFIcwKWBwc",
    "kty": "RSA",
    "q": "0GoU4cNQ0pvHYEgL_sMum_Il7Fdwn1ZYjS-kjahVZFvQtGHq_y5QWZMfOh0b_lPd4jrJogY-4KGuLmoNXgaRFzo0vfYW64VwIPFC7Lflg2JvGna1ssghj_4aFA-k8d9QZGRzEO7Pvj4AusxbOfOy0937du9qx7G1wAhg8bsYesk",
    "d": "QIHOUj7Rdmug6_PRaARWqDEPL8pAVbHMLJNXPU1Jc_YrVDFN5CqFxFZyPGRDye4tNsbSYRZt8HGSHAf-Bta7LiXlM9ar7FhWF6xz_X1bGRS5d67vhvW8Xsm3c1GEoKnZpGy9sf__N8smVg5zXkGMiVBh5N0dWpWbiOkBNbyUGb68HVqTNxJ1eA7eyqhk_GY7C5FhehQ5uurbX4ehgyriD7kyK4bfYK7lh905vOOvL23-f_sxkQBbQa9ZkQ2YW_yxgBvUI9a9SdBCrGsRrpjMf1mvQTIQukph9BJZcSfs7rTLS2Utfaba4JDyApeCL4h1N1DWdeT_egrw9dVSoPW5AQ",
    "e": "AQAB",
    "use": "sig",
    "kid": "sig-1692258470",
    "qi": "1oCP5gxE8BDHekikod7Hj8F33rIw8D5SJWhoZY2ov63_RgTNk8kZcS5uh0UktRtF2dofbVDTGh7EnaNRmMK9UPOmt3aLf3TcSYu82SqcR1cpsXzIk1u6oS8c5heQ-jE_eoxMuQCv_ZH4fqxqrw4rmX_Qs2DiHfR329pX3gERvN0",
    "dp": "PhKYWb3bq05bQGYRY0toJPPQrMH7GYCuEywZbbFHylNA0a1so5_1E7fmErGP1eMDoQLwo5OnfAijVkEgy5drTD_4ocVaMGoqfG23iBmKTOV5gN42N4-auo_8IHSQelj1H1TDvb8p6sQtbwcJWoJ5GfxitZSgIRau9bvy4ptQ9hE",
    "alg": "RS256",
    "dq": "SQjDpJHDYuqAJbdZrL9NOAzVSUsjBlNF2MQXUCTrN64NJwkhRqc-NQWfbcgBpVBScxLS0dqKckF2PoGfiZGXiqI1FVSFl6c9Me4Z28ZdwXrfIFD1P19uk30iOmF5FeGB1Ix23joxxqMHsm4mkdpaknA5zOX9b1lRLahCALPl0jE",
    "n": "wv_8dUqrzJOkFKY6JCdIIVfAJteSCstPhTCZm4rxd5aRmS6wtstn5eIJqz9LLDuY5xvhfJvbDQfGudZdgal-c6NGZZh2rv_XAJjLBzH6mNeZXmAPwDQvGNJaRgKMx02VO_dVkgP7XmYAA6VsyOP6FR-vAtJ-fClyqbZv1OXa2wKTHVQLRBXWONRJtpZgEfseyZfZqTN4H-IH-nz9iEubbZ2q8zfVO5JPLvZvBnU-_MNMm352PUQTP2wjWsxYdK93XVAc1omunRIUHzhRxm2gNCP33Gs5NzgYWQe5qogY8wA4GMetWOxqjNfr4iebGlEGL4Mf8ksJBlqNG8RSTMzafw"
})


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
    token = jwt.encode(payload, key.to_dict(), algorithm='RS256')
    return {"access_token": token}


@app.get("/.well-known/jwks.json")
async def jwks():
    return {
        "keys": [key.to_dict()]
    }
