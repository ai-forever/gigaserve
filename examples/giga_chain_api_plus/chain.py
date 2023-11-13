from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models.gigachat import GigaChat
from langchain.prompts import load_prompt
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
chain.save("chain.yaml")
