from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import openai
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# MongoDB model
class Item(BaseModel):
    name: str
    description: str

# Initialize MongoDB
# @app.on_event("startup")
# async def startup_event():
#     client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
#     await init_beanie(database=client.mydatabase, document_models=[Item])

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

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

@app.post("/generate_description/")
async def generate_description(prompt: str):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100
    )
    return {"generated_description": response.choices[0].text.strip()}