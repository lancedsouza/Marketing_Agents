from typing import Annotated, List, TypedDict
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    job_description: str
    extracted_skills: List[str]
    candidates: List[dict]
    iteration_count: int

from pydantic import BaseModel, Field

class SkillSearchSchema(BaseModel):
    query: str = Field(description="The semantic skill to search for (e.g., 'Python programming')")
    top_k: int = Field(default=5, description="Number of related ESCO skills to return")

# This "Contract" ensures the LLM doesn't send a random string