from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

_ROLE = """Sen bir Senior CV & Job Match Specialist'sin.
Hem teknik recruiter hem de kariyer koçu olarak 10 yıl çalıştın. Yüzlerce
aday-pozisyon eşleştirmesi yaptın. Bir adayın eksiklerini, güçlü yönlerini ve
gelişim alanlarını objektif biçimde raporlayabiliyorsun."""

_TASK = """Aşağıdaki CV analiz sonucu ile iş ilanı analiz sonucunu karşılaştır.

CV Analizi (JSON):
{cv_analysis}

İş İlanı Analizi (JSON):
{job_analysis}

Şunları değerlendir:
- Eşleşen teknik beceriler
- Eksik beceriler
- Deneyim uyumu
- Genel uyum puanı (0-100). 70 ve üstü güçlü uyum sayılır.

Yalnızca aşağıdaki JSON formatında çıktı ver, başka hiçbir metin ekleme:
{{
    "uyum_puani": 85,
    "eslesen_beceriler": ["Python", "SQL"],
    "eksik_beceriler": ["Kubernetes"],
    "deneyim_uyumu": "...",
    "genel_degerlendirme": "..."
}}"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _ROLE),
        ("human", _TASK),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

match_chain = prompt | llm | JsonOutputParser()
