from openai import OpenAI

from errors import ApiBotException
from models import QueryPrompt
from typing import List
import os

DEFAULT_MODEL_TEMPERATURE = 0.25
DEFAULT_MODEL_LLM = "gpt-3.5-turbo"
ENABLE_LLM_API_MOCK = False

openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_completion(query_prompt: QueryPrompt, context: List[QueryPrompt], model: str, temperature: float):
    anonymous_prompt = (". Please remove any private information such as name, age, address"
                        "and any other personally identifiable information in the request or response")

    messages = context + [QueryPrompt(role=query_prompt.role, content=query_prompt.content + anonymous_prompt)]

    if ENABLE_LLM_API_MOCK:
        return "This is a mock chat GPT!"

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except:
        raise ApiBotException(code=422, message="Unable to create resource")
