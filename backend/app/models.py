from pydantic import BaseModel
from beanie import Document
from typing import List
from enum import Enum


class QueryRoleType(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"
    function = "function"

class QueryPrompt(BaseModel):
    role: QueryRoleType
    content: str

class Message(BaseModel):
    user_message: QueryPrompt
    llm_message: str


class LlmParams(BaseModel):
    model_name: str
    temperature: float


class ConversationModel(Document):
    name: str
    llm_params: LlmParams
    messages: List[Message] = []


class ConversationListingModel(BaseModel):
    id: str
    name: str
