#!/usr/bin/env python
"""Example LangChain server exposes a chain composed of a prompt and an LLM."""
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models.gigachat import GigaChat
from langchain.prompts import load_prompt
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langserve import add_routes

logging.basicConfig(level=logging.INFO)


giga = GigaChat(profanity=False, verbose=True, timeout=30, verify_ssl_certs=False)

map_prompt = load_prompt("lc://prompts/summarize/map_reduce/map.yaml")
combine_prompt = load_prompt("lc://prompts/summarize/map_reduce/combine.yaml")

splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
combine_chain = load_summarize_chain(
    giga,
    chain_type="map_reduce",
    map_prompt=map_prompt,
    combine_prompt=combine_prompt,
)

chain = AnalyzeDocumentChain(combine_docs_chain=combine_chain, text_splitter=splitter)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from contextvars_executor import ContextVarExecutor

    # contextvars friendly ThreadPoolExecutor
    loop = asyncio.get_running_loop()
    loop.set_default_executor(ContextVarExecutor())
    yield


app = FastAPI(
    title="GigaChain Server",
    version="1.0",
    description="Spin up a simple api server using GigaChain's Runnable interfaces",
    lifespan=lifespan,
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.middleware("http")
async def gigachat_headers(request, call_next):
    from gigachat.context import (
        authorization_cvar,
        client_id_cvar,
        request_id_cvar,
        session_id_cvar,
    )

    # forwarding headers to gigachat
    authorization_cvar.set(request.headers.get("Authorization"))
    client_id_cvar.set(request.headers.get("X-Client-ID"))
    session_id_cvar.set(request.headers.get("X-Session-ID"))
    request_id_cvar.set(request.headers.get("X-Request-ID"))

    return await call_next(request)


add_routes(app, chain, path="/summarize")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
