# services/openai_api.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_gpt(message: str, persona: str) -> str:
    try:
        prompt = f"{persona}\nПользователь: {message}\nПерсонаж:"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": persona},
                      {"role": "user", "content": message}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Ошибка AI: {str(e)}"
