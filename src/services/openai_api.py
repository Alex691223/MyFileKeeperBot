# services/openai_api.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def ask_gpt(message: str, persona: str) -> str:
    try:
        system_prompt = persona

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Ошибка AI: {e}"
