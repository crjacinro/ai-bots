from openai import OpenAI
from pydantic import BaseModel
import os

MODEL_TEMPERATURE = 0.25
MODEL_LLM = "gpt-3.5-turbo"
ENABLE_LLM_API_MOCK = True

# Set OpenAI API key
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class QueryPrompt(BaseModel):
    role: str
    content: str

def get_completion(query_prompt: QueryPrompt, model=MODEL_LLM):
    messages = [{"role": query_prompt.role, "content": query_prompt.content}]

    if ENABLE_LLM_API_MOCK:
        return "This is a mock chat GPT!"

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=MODEL_TEMPERATURE
    )
    return response.choices[0].message.content
