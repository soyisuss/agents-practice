from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

model = init_chat_model("deepseek:deepseek-chat")


class SecurityReview(BaseModel):
    vulnerabilities: list[str] = Field(
        description="The vulnerabilities in the code", default=[]
    )
    riskLevel: str = Field(
        description="Severity of the vulnerability, e.g. 'High', 'Medium', 'Low'",
        default="",
    )
    suggestions: str = Field(
        description="The suggestions for fixing the vulnerabilities", default=""
    )


class MaintainabilityReview(BaseModel):
    concerns: list[str] = Field(
        description="The vulnerabilities in the code", default=[]
    )
    qualityScore: int = Field(
        description="The quality score of the code, from 0 to 10", default=0
    )
    recommendations: str = Field(
        description="The recommendations for improving the code", default=""
    )


class State(TypedDict):
    code: str
    security_review: SecurityReview
    maintainability_review: MaintainabilityReview
    final_review: str


def security_review(state: State):
    code = state["code"]
    messages = [
        (
            "system",
            "You are an expert in code security. Focus on identifying security vulnerabilities, injection risks, and authentication issues.",
        ),
        ("user", f"Review this code: {code}"),
    ]
    llm_with_structured_output = model.with_structured_output(SecurityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {"security_review": schema}


def maintainability_review(state: State):
    code = state["code"]
    messages = [
        (
            "system",
            "You are an expert in code quality. Focus on code structure, readability, and adherence to best practices.",
        ),
        ("user", f"Review this code: {code}"),
    ]
    llm_with_structured_output = model.with_structured_output(MaintainabilityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {"maintainability_review": schema}


def aggregator(state: State):
    security_review = state["security_review"]
    maintainability_review = state["maintainability_review"]
    messages = [
        ("system", "You are a technical lead summarizing multiple code reviews"),
        (
            "user",
            f"Synthesize these code review results into a concise summary with key actions: Security review: {security_review} and Maintainability review: {maintainability_review}",
        ),
    ]
    response = model.invoke(messages)
    return {"final_review": response.text}


builder = StateGraph(State)

builder.add_node("security_check", security_review)
builder.add_node("maintainability_check", maintainability_review)
builder.add_node("aggregator", aggregator)

builder.add_edge(START, "security_check")
builder.add_edge(START, "maintainability_check")
builder.add_edge("security_check", "aggregator")
builder.add_edge("maintainability_check", "aggregator")
builder.add_edge("aggregator", END)

agent = builder.compile()
