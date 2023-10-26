#!/usr/bin/env python
"""Example LangChain server exposes a chain composed of a prompt and an LLM."""
import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models.gigachat import GigaChat
from langchain.prompts import load_prompt
from langchain.text_splitter import CharacterTextSplitter

from langserve import add_routes

user = os.environ.get("GIGA_USER", None)
password = os.environ.get("GIGA_PASSWORD", None)

logging.basicConfig(level=logging.INFO)


def build_chain():
    giga = GigaChat(
        profanity=False,
        verbose=True,
        verify_ssl_certs=False,
        user=user,
        password=password,
        base_url="https://wmapi-dev.saluteai-pd.sberdevices.ru/v1",
        model="GigaChat-70b-4k-base:latest",
        timeout=30,)

    map_prompt = load_prompt("lc://prompts/summarize/map_reduce/map.yaml")
    combine_prompt = load_prompt("lc://prompts/summarize/map_reduce/combine.yaml")

    splitter = CharacterTextSplitter(chunk_size=12000, chunk_overlap=1000)
    combine_chain = load_summarize_chain(
        giga,
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=combine_prompt,
    )
    return AnalyzeDocumentChain(
        combine_docs_chain=combine_chain, text_splitter=splitter
    )

chain = build_chain()

app = FastAPI(
    title="GigaChain Server",
    version="1.0",
    description="Spin up a simple api server using GigaChain's Runnable interfaces",
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

add_routes(app, chain)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
