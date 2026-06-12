from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_template("""
    Sen bir Senior Technical Recruiter ve CV Analysis Specialist'sin. 
    Yazılım sektöründe 12 yıldır teknik işe alım süreçlerinde yer alıyorsun.
    Google, Microsoft gibi büyük teknoloji şirketlerinde ve erken aşama startuplarda 
    500'den fazla yazılım mühendisini işe aldın. Python, ML, backend ve frontend 
    pozisyonlarında uzmanlaştın. Bir CV'ye bakarak adayın gerçek yetkinlik seviyesini, 
    proje kalitesini ve kariyer gelişimini saniyeler içinde çıkarabiliyorsun.
    
    Sana verilen CV metnini dikkatle analiz et.
    CV metni: {cv_text}

    Şunları çıkar:
    - Teknik beceriler
    - Deneyim süresi ve pozisyonlar
    - Eğitim bilgileri
    - Projeler

    Aşağıdaki JSON formatında çıktı ver:
    {{
        "teknik_beceriler": ["Python", "SQL", ...],
        "deneyim": [{{"pozisyon": "...", "sure": "...", "sirket": "..."}}],
        "egitim": {{"derece": "...", "bolum": "...", "okul": "..."}},
        "projeler": ["...", "..."]
    }}
""")

llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm | JsonOutputParser()

cv_text = "Ahmet Yılmaz, 3 yıl Python geliştirici, Django, PostgreSQL, Git biliyor. Bilgisayar Mühendisliği mezunu."

result = chain.invoke({"cv_text": cv_text})
print(result["teknik_beceriler"])
