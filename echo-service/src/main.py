from typing import Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/echo_user_info")
async def echo_user_info(username: Optional[str] = Header(None)):
    return {"username": username}
