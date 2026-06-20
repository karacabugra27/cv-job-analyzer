from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

_ROLE = """Sen bir Senior Career Coach ve Professional Cover Letter Writer'sın.
10 yıldır kariyer koçluğu yapıyorsun. Yazdığın cover letter'lar adayların işe
alınma oranını 3 katına çıkardı. Her cover letter'ı adayın güçlü yönlerini ön
plana çıkaracak şekilde yazıyorsun."""

_TASK = """Aşağıdaki analiz sonuçlarına göre kişiselleştirilmiş bir cover letter yaz.

CV Analizi (JSON):
{cv_analysis}

İş İlanı Analizi (JSON):
{job_analysis}

Uyum Analizi (JSON):
{match_analysis}

Kurallar:
- Güçlü yönleri ön plana çıkar
- Eksikleri fırsata çevir
- Profesyonel ve ikna edici bir dil kullan
- 3 paragraf:
  * Paragraf 1: Güçlü giriş ve pozisyona ilgi
  * Paragraf 2: Eşleşen beceriler ve deneyimler
  * Paragraf 3: Motivasyon ve kapanış

Sadece cover letter metnini döndür, başka açıklama ekleme."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _ROLE),
        ("human", _TASK),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

cover_letter_chain = prompt | llm | StrOutputParser()
