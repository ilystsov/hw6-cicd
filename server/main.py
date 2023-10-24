from typing import Dict, Callable, Awaitable
import re
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import PlainTextResponse, JSONResponse

app = FastAPI()

allowed_endpoints = [
    r"^/hello$",
    r"^/get/\w+$",
    r"^/set$",
    r"^/divide$",
    r"^/docs$",
    r"^/openapi.json$",
]

data_storage: Dict[str, str] = {}


@app.get("/hello")
async def read_hello() -> PlainTextResponse:
    return PlainTextResponse("HSE One Love!")


def check_json_header(header: str | None) -> None:
    if header != 'application/json':
        raise HTTPException(status_code=415, detail="")


@app.post("/set")
async def save_data(request: Request) -> PlainTextResponse:
    check_json_header(request.headers.get('content-type'))
    try:
        data = await request.json()
        key = data["key"]
        value = data["value"]
    except Exception as exc:
        raise HTTPException(status_code=400, detail="") from exc
    data_storage[key] = value
    return PlainTextResponse("Data saved.")


@app.get("/get/{key}")
async def read_key(key: str) -> JSONResponse:
    if key in data_storage:
        value = data_storage[key]
        return JSONResponse(content={"key": f"{key}", "value": f"{value}"})
    raise HTTPException(status_code=404, detail="")


@app.post("/divide")
async def divide(request: Request) -> PlainTextResponse:
    check_json_header(request.headers.get('content-type'))
    try:
        data = await request.json()
        dividend = data["dividend"]
        divider = data["divider"]
        result = float(dividend) / float(divider)
        return PlainTextResponse(str(result))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="") from exc


@app.middleware("http")
async def handle_other_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    path = request.url.path
    if not any(re.match(allowed, path) for allowed in allowed_endpoints):
        return JSONResponse(status_code=405, content={"detail": ""})
    response = await call_next(request)
    if response.status_code == 405:
        return JSONResponse(status_code=405, content={"detail": ""})
    return response
