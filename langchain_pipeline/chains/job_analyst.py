from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

_ROLE = """Sen bir Senior Job Market Analyst ve Technical Requirements Specialist'sin.
Yazılım sektöründe 15 yılı aşkın süredir hem işveren hem recruiter perspektifinden iş ilanlarını
analiz ediyorsun. Google, Microsoft gibi büyük teknoloji şirketlerinde ve erken aşama
startuplarda işe alım süreçleri tasarladın. Bir iş ilanındaki gerçek gereksinimleri,
gizli beklentileri ve şirket kültürünü saniyeler içinde okuyabiliyorsun."""

_TASK = """Sana verilen iş ilanı metnini dikkatle analiz et.
İlan metni:
{job_text}

Şunları çıkar:
- Zorunlu teknik beceriler
- Tercih edilen teknik beceriler
- Beklenen deneyim süresi ve pozisyon seviyesi
- Şirket kültürü ve çalışma biçimi

Yalnızca aşağıdaki JSON formatında çıktı ver, başka hiçbir metin ekleme:
{{
    "zorunlu_beceriler": ["Python", "SQL"],
    "tercih_edilen": ["Docker", "Kubernetes"],
    "deneyim": [{{"pozisyon": "...", "sure": "..."}}],
    "sirket_kulturu": ["...", "..."]
}}"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _ROLE),
        ("human", _TASK),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

job_chain = prompt | llm | JsonOutputParser()
