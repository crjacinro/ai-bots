from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from beanie import Document, Indexed, init_beanie
import os

app = FastAPI()

# MongoDB model
class Item(Document):
    name: str
    description: str

#Initialize MongoDB
@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
    await init_beanie(database=client.mydatabase, document_models=[Item])

# Set OpenAI API key
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    await item.insert()
    return {"message": "Item created successfully"}

@app.get("/items/", response_model=List[Item])
async def get_items():
    items = await Item.find_all().to_list()
    return items





class QueryPrompt(BaseModel):
    role: str = None
    content: str = None

@app.post("/queries/{id}")
async def queries(id: str, query_prompt: QueryPrompt):
    response = get_completion(query_prompt)
    return {"response": response.strip()}

def get_completion(query_prompt: QueryPrompt, model="gpt-3.5-turbo"):
    messages = [{"role": query_prompt.role, "content": query_prompt.content}]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.25
    )
    return response.choices[0].message.content