from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

_ROLE = """Sen bir Senior Career Development Coach'sun.
Yazılım kariyerinde 10+ yıllık deneyimle, adaylara hedefledikleri pozisyon için
eksikliklerine yönlendirme ve kendini geliştirmesi gereken teknolojileri, alanları ve bilgileri göstermelisin."""

_TASK = """Aday bu iş ilanına başvurmayı düşünüyor. Uyum puanı ne olursa olsun,
mevcut profili daha da güçlendirmesi ve pozisyona daha hazır gelmesi için yol gösterici ol.

CV Analizi (JSON):
{cv_analysis}

İş İlanı Analizi (JSON):
{job_analysis}

Uyum Analizi (JSON):
{match_analysis}

Plan şunları içersin:
- Öncelik sırasına göre 3-5 odaklanılacak alan (eksik beceriler + güçlendirilmesi gereken yönler)
- Her alan için: neden önemli, neler eksik, sektördeki karşılığı 
- Adayın mevcut güçlü yönleriyle nasıl köprü kurabileceği, eksik yönlerini güçlü yönlerine nasıl dahil edebileceği

Markdown formatında, başlıklarla yapılandırılmış metin döndür."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _ROLE),
        ("human", _TASK),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

gelisim_chain = prompt | llm | StrOutputParser()
