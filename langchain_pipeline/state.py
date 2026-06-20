from typing import TypedDict


class GraphState(TypedDict):
    cv_text: str
    job_text: str
    cv_analysis: dict
    job_analysis: dict
    match_analysis: dict
    gelisim_onerileri: str
