from openai import OpenAI
from pydantic import BaseModel
from enum import Enum
import os

MODEL_TEMPERATURE = 0.25
MODEL_LLM = "gpt-3.5-turbo"
ENABLE_LLM_API_MOCK = True

openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class QueryRoleType(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"
    function = "function"

class QueryPrompt(BaseModel):
    role: QueryRoleType
    content: str

def get_completion(query_prompt: QueryPrompt, model: str, temperature: float):
    messages = [{"role": query_prompt.role, "content": query_prompt.content}]

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


