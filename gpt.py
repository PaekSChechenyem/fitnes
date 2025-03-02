from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from auth import api_key

client = AsyncOpenAI(
    api_key=api_key,
)

async def generate_answer(text) -> ChatCompletion:
        chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="gpt-4o-mini",
    )
        return chat_completion