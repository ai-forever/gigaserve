"""Пример вызова суммаризации статьи "Великий аттрактор" из Википедии"""
import requests
import yaml

with open("chain.yaml", "r", encoding="utf-8") as f:
    CHAIN_CONFIG = yaml.safe_load(f)

with open("attractor.txt", "r", encoding="utf-8") as f:
    TEXT = f.read()

with open("access_token.txt", "r", encoding="utf-8") as f:
    ACCESS_TOKEN = f.read().strip()

# Пример обращения с помощью requests
response = requests.post(
    "http://localhost:8000/chain_invoke",
    json={"chain_config": CHAIN_CONFIG, "input": {"input_document": TEXT}},
    timeout=600,
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        # for logging
        "X-Client-ID": "8324244b-7133-4d30-a328-31d8466e5502",
        "X-Session-ID": "8324244b-7133-4d30-a328-31d8466e5502",
        "X-Request-ID": "8324244b-7133-4d30-a328-31d8466e5502",
    },
)

print(response.status_code)
resp = response.json()
print(resp)
