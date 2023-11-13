#!/usr/bin/env python
"""Example LangChain server API+."""
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any

import fastapi
from gigachat.exceptions import AuthenticationError
from langchain.pydantic_v1 import BaseModel
from langchain.chains.loading import load_chain_from_config
import yaml
from contextvars_executor import ContextVarExecutor
from gigachat.context import (
    authorization_cvar,
    client_id_cvar,
    request_id_cvar,
    session_id_cvar,
)

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app):
    loop = asyncio.get_running_loop()
    loop.set_default_executor(ContextVarExecutor())
    yield


app = fastapi.FastAPI(lifespan=lifespan)


@app.middleware("http")
async def middleware(request, call_next):
    # forwarding headers to gigachat
    authorization_cvar.set(request.headers.get("Authorization"))
    client_id_cvar.set(request.headers.get("X-Client-ID"))
    session_id_cvar.set(request.headers.get("X-Session-ID"))
    request_id_cvar.set(request.headers.get("X-Request-ID"))

    return await call_next(request)


class Payload(BaseModel):
    chain_yaml: str
    input: dict[str, Any]


class Result(BaseModel):
    output: dict[str, Any]


@app.post("/chain_invoke")
def chain_invoke(payload: Payload) -> Result:
    config = yaml.safe_load(payload.chain_yaml)
    chain = load_chain_from_config(config)
    try:
        output = chain.invoke(input=payload.input)
        return Result(output=output)
    except AuthenticationError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Wrong token"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
