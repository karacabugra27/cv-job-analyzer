from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

_ROLE = """Sen bir Senior Technical Interview Coach'sun.
FAANG şirketlerinde 8 yıl teknik mülakatçı olarak çalıştın. Binlerce mülakat
yaptın. Hangi soruların sorulacağını ve ideal cevapların nasıl olması gerektiğini
çok iyi biliyorsun."""

_TASK = """Aşağıdaki analiz sonuçlarına göre muhtemel mülakat soruları hazırla.

CV Analizi (JSON):
{cv_analysis}

İş İlanı Analizi (JSON):
{job_analysis}

Uyum Analizi (JSON):
{match_analysis}

Şunları üret:
- Teknik sorular (5-7 adet, eksik becerilere ve mevcut deneyime odaklı)
- Davranışsal sorular (3-5 adet)
- Her soru için ideal cevap stratejisi

Yalnızca aşağıdaki JSON formatında çıktı ver, başka hiçbir metin ekleme:
{{
    "teknik_sorular": [
        {{"soru": "...", "ideal_cevap_stratejisi": "..."}}
    ],
    "davranissal_sorular": [
        {{"soru": "...", "ideal_cevap_stratejisi": "..."}}
    ]
}}"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _ROLE),
        ("human", _TASK),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

interview_chain = prompt | llm | JsonOutputParser()
