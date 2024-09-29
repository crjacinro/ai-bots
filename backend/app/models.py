from llm import QueryRoleType
from pydantic import BaseModel
from beanie import Document
from typing import List

class Messages(BaseModel):
    role: QueryRoleType
    user_message: str
    llm_message: str


class LlmParams(BaseModel):
    model_name: str
    temperature: float


class ConversationModel(Document):
    name: str
    llm_params: LlmParams
    messages: List[Messages] = []


class ConversationListingModel(BaseModel):
    id: str
    name: str
