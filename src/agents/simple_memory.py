from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    user_name: NotRequired[str]
    user_age: NotRequired[int]


state: State = {}
user_name = state.get("user_name", None)


def node_1(state: State):
    if state.get("user_name") is None:
        return {"user_name": "Yael"}
    return {}


# Intialize using the custom state
builder = StateGraph(State)
# Add the node
builder.add_node("node_1", node_1)
# Defin the conections between nodes using the START and END node
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)
# Compile the Graph
agent = builder.compile()
