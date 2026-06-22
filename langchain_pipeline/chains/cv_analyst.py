from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

_ROLE = """Sen bir Senior Technical Recruiter ve CV Analysis Specialist'sin.
Yazılım sektöründe 15 yıldır teknik işe alım süreçlerinde yer alıyorsun.
Google, Microsoft gibi büyük teknoloji şirketlerinde ve erken aşama startuplarda
500'den fazla yazılım mühendisini işe aldın. Backend, frontend, mobil, veri ve
ML dahil tüm yazılım pozisyonlarında derin bilgi birikimine sahipsin.
Bir CV'ye bakarak adayın gerçek yetkinlik seviyesini, proje kalitesini,
deneyim süresini ve kariyer gelişimini saniyeler içinde çıkarabiliyorsun."""

_TASK = """Sana verilen CV metnini dikkatle analiz et.
CV metni:
{cv_text}

Şunları çıkar:
- Teknik beceriler
- Deneyim süresi ve pozisyonlar
- Eğitim bilgileri
- Projeler

Teknik becerileri çıkarırken şuna dikkat et:
- Bir teknolojinin kullanımı başka bir teknolojiyi zorunlu kılıyorsa, ikisini de listele.
  Örneğin Spring Boot varsa Java'yı, React varsa JavaScript'i, Django varsa Python'u da ekle.
- CV'de açıkça yazılmasa bile projelerden/deneyimden çıkarılabilen becerileri ekle.

Yalnızca aşağıdaki JSON formatında çıktı ver, başka hiçbir metin ekleme:
{{
    "teknik_beceriler": ["Python", "SQL"],
    "deneyim": [{{"pozisyon": "...", "sure": "...", "sirket": "..."}}],
    "egitim": {{"derece": "...", "bolum": "...", "okul": "..."}},
    "projeler": ["...", "..."]
}}"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _ROLE),
        ("human", _TASK),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

cv_chain = prompt | llm | JsonOutputParser()
