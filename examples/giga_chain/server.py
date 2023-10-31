#!/usr/bin/env python
"""Example LangChain server exposes a chain composed of a prompt and an LLM."""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models.gigachat import GigaChat
from langchain.prompts import load_prompt
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langserve import add_routes

logging.basicConfig(level=logging.INFO)


giga = GigaChat(profanity=False, verbose=True, timeout=30)

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

add_routes(app, chain, path="/summarize")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
