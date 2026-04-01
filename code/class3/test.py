import json
from openai import OpenAI

def load_config():
    with open("code\class3\config.json", "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

client = OpenAI(
    api_key=config["OPENAI_API_KEY"],
    base_url=config["OPENAI_BASE_URL"]
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system",
            "name": "AI助手",
            "content": "你是一个友好、专业的AI助手"
        },
        {
            "role": "user",
            "name": "用户",
            "content": "你好，请介绍一下你自己"
        }
    ],
    temperature=1.0,
    top_p=0.95,
    max_completion_tokens=2048
)

print(response.choices[0].message.content)