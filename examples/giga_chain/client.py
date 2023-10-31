"""Пример вызова суммаризации статьи "Великий аттрактор" из Википедии"""
import requests

with open("attractor.txt", "r", encoding="utf-8") as f:
    TEXT = f.read()

with open("access_token.txt", "r", encoding="utf-8") as f:
    ACCESS_TOKEN = f.read().strip()

# Пример обращения с помощью requests
response = requests.post(
    "http://localhost:8000/summarize/invoke",
    json={"input": {"input_document": TEXT}},
    timeout=600,
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        # for logging
        "X-Client-ID": "8324244b-7133-4d30-a328-31d8466e5502",
        "X-Session-ID": "8324244b-7133-4d30-a328-31d8466e5502",
        "X-Request-ID": "8324244b-7133-4d30-a328-31d8466e5502",
    }
)
resp = response.json()
print(resp["output"]["output_text"])
