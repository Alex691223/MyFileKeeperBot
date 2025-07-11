import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_reply(persona_prompt: str, user_message: str) -> str:
    prompt = f"{persona_prompt}\n\nПользователь: {user_message}\nПерсонаж:"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": persona_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content.strip()
