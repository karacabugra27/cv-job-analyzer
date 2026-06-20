import json

from langchain_pipeline.state import GraphState
from langchain_pipeline.chains.cv_analyst import cv_chain
from langchain_pipeline.chains.job_analyst import job_chain
from langchain_pipeline.chains.match_analyst import match_chain
from langchain_pipeline.chains.gelisim_onerileri import gelisim_chain


def cv_analiz_node(state: GraphState) -> GraphState:
    state["cv_analysis"] = cv_chain.invoke({"cv_text": state["cv_text"]})
    return state


def job_analiz_node(state: GraphState) -> GraphState:
    state["job_analysis"] = job_chain.invoke({"job_text": state["job_text"]})
    return state


def match_analiz_node(state: GraphState) -> GraphState:
    state["match_analysis"] = match_chain.invoke(
        {
            "cv_analysis": json.dumps(state["cv_analysis"], ensure_ascii=False),
            "job_analysis": json.dumps(state["job_analysis"], ensure_ascii=False),
        }
    )
    return state


def gelisim_node(state: GraphState) -> GraphState:
    state["gelisim_onerileri"] = gelisim_chain.invoke(
        {
            "cv_analysis": json.dumps(state["cv_analysis"], ensure_ascii=False),
            "job_analysis": json.dumps(state["job_analysis"], ensure_ascii=False),
            "match_analysis": json.dumps(state["match_analysis"], ensure_ascii=False),
        }
    )
    return state
