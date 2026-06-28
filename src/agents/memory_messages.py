from langgraph.graph import MessagesState, StateGraph, START, END
from langchain.messages import AIMessage


class State(MessagesState):
    user_name: str
    user_age: int


def node_1(state: State):
    if state.get("user_name") is None:
        return {"user_name": "Yael"}
    else:
        return {"messages": [AIMessage("How can I help you?")]}


# Intialize using the custom state
builder = StateGraph(State)
# Add the node
builder.add_node("node_1", node_1)
# Defin the conections between nodes using the START and END node
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)
# Compile the Graph
agent = builder.compile()
