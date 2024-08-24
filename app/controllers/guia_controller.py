from openai import OpenAI
from app.config import config

# Configura el cliente OpenAI
client = OpenAI(base_url=config.OPENAI_BASE_URL, api_key=config.OPENAI_API_KEY)

async def get_chat_response(messages: list, model: str = "lmstudio-community/Phi-3.1-mini-4k-instruct-GGUF", temperature: float = 0.7) -> dict:
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return completion.choices[0].message
    except Exception as e:
        return {"error": str(e)}
