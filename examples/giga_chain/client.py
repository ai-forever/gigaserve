"""Пример вызова суммаризации статьи "Великий аттрактор" из Википедии"""
import requests

with open("examples/giga_chain/attractor.txt", "r", encoding="utf-8") as f:
    TEXT = str(f.read())

# Пример обращения с помощью requests
response = requests.post(
    "http://localhost:8000/summarize/invoke",
    json={"input": {"input_document": TEXT}},
    timeout=600,
)
resp = response.json()
print(resp["output"]["output_text"])
