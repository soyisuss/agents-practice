from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal, cast
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model


class State(TypedDict):
    joke: str
    topic: str
    feedback: str
    is_funny: bool


class Feedback(BaseModel):
    is_funny: bool = Field(
        description="Is the joke funny?, Return True if it is, or False otherwise"
    )
    feedback: str = Field(description="Feedback for the joke on how to improve it")


model = init_chat_model("deepseek:deepseek-chat")
evaluator_model = model.with_structured_output(Feedback)


def generator_node(state: State):
    feedback = state.get("feedback", None)
    topic = state.get("topic", None)
    if feedback:
        msg = model.invoke(
            f"Write a joke bout {topic} but take into account the feedback: {feedback}, respond in spanish"
        )
    else:
        msg = model.invoke(f"Write a joke bout {topic}, respond in spanish")
    return {"joke": msg.content}


def evaluator_node(state: State):
    joke = state.get("joke", None)
    schema = cast(Feedback, evaluator_model.invoke(f"Grade the joke {joke}"))
    return {"is_funny": schema.is_funny, "feedback": schema.feedback}


def route_edge(state: State) -> Literal["__end__", "generator_node"]:
    is_funny = state.get("is_funny", True)
    if is_funny:
        return "__end__"
    else:
        return "generator_node"


builder = StateGraph(State)

builder.add_node("generator_node", generator_node)
builder.add_node("evaluator_node", evaluator_node)

builder.add_edge(START, "generator_node")
builder.add_edge("generator_node", "evaluator_node")
builder.add_conditional_edges("evaluator_node", route_edge)
agent = builder.compile()
