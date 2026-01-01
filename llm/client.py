from typing import Dict, Any, Optional
import json
import time
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv(override=True)

from openai import OpenAI

client = OpenAI()

def call_llm(
    *,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.0,
    max_tokens: int = 2048,
    response_format: Optional[str] = None,
    retries: int = 1
) -> str:
    """
    Deterministic LLM invocation with retries.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    for attempt in range(retries):
        print(messages)
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=(
                    {"type": "json_object"} if response_format == "json" else None
                )
            )

            content = response.choices[0].message.content
            print(content)
            return content

        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
