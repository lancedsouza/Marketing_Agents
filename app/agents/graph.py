from langgraph.graph import StateGraph, END
from app.agents.hiring_detector import detect_hiring_quality
from app.agents.contact_finder import find_founder_details

def build_recruitment_graph():
    workflow = StateGraph(ScoutState) # Your defined state

    # Add the nodes (The Workers)
    workflow.add_node("detect_hiring", detect_hiring_quality)
    workflow.add_node("find_contact", find_founder_details)

    # Define the edges (The Flow)
    workflow.set_entry_point("detect_hiring")

    # Conditional Logic: Only find contact if it's a Senior Role
    workflow.add_conditional_edges(
        "detect_hiring",
        lambda x: "continue" if x["is_senior"] else "end",
        {
            "continue": "find_contact",
            "end": END
        }
    )

    workflow.add_edge("find_contact", END)
    return workflow.compile()