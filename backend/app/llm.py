from openai import OpenAI
from models import QueryPrompt
import os

DEFAULT_MODEL_TEMPERATURE = 0.25
DEFAULT_MODEL_LLM = "gpt-3.5-turbo"
ENABLE_LLM_API_MOCK = False

openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
