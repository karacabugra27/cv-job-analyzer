from langgraph.graph import StateGraph, END

from langchain_pipeline.state import GraphState
from langchain_pipeline.nodes import (
    cv_analiz_node,
    job_analiz_node,
    match_analiz_node,
    gelisim_node,
)


def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("cv_analiz", cv_analiz_node)
    workflow.add_node("job_analiz", job_analiz_node)
    workflow.add_node("match_analiz", match_analiz_node)
    workflow.add_node("gelisim", gelisim_node)

    workflow.set_entry_point("cv_analiz")
    workflow.add_edge("cv_analiz", "job_analiz")
    workflow.add_edge("job_analiz", "match_analiz")
    workflow.add_edge("match_analiz", "gelisim")
    workflow.add_edge("gelisim", END)

    return workflow.compile()


graph = build_graph()
