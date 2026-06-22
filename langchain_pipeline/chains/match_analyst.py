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

Değerlendirirken şu kurallara mutlaka uy:
- Eksik beceri belirlerken transferable / ilgili teknolojileri eksik gösterme.
  Örnekler (eksik sayma):
  * Aday PostgreSQL veya MySQL biliyorsa "SQL" eksik değildir.
  * Aday Spring Boot biliyorsa "Java" eksik değildir.
  * Aday React biliyorsa "JavaScript" eksik değildir.
  * Aday Django/Flask/FastAPI biliyorsa "Python" eksik değildir.
  * Aday TensorFlow/PyTorch biliyorsa "Machine Learning" eksik değildir.
  Kısacası: bir üst-teknoloji veya temel dil, alt-framework/araç biliniyorsa otomatik karşılanmış sayılır.
- "eksik_beceriler" sadece adayda hiç olmayan VE iş ilanında zorunlu/önemli olan becerileri içermeli.
- Deneyim süresi uyum puanının BAĞIMSIZ bir bileşenidir. Adayın teknik becerileri
  ne kadar güçlü olursa olsun, ilanın talep ettiği yıl sayısı karşılanmıyorsa
  uyum puanı buna göre düşürülmelidir. Teknik beceri eşleşmesi tek başına
  yüksek puanı garantilemez.
- Deneyim farkı kuralları:
  * 0-1 yıl açık → puanı etkilemez.
  * 2 yıl açık → orta düzey ceza (puanı belirgin düşür, 80+ olamaz).
  * 3+ yıl açık veya pozisyon seviyesi farkı (Senior pozisyona junior/mid başvuru)
    → büyük ceza (puanı 60'ın altına çek, "tecrübe yetersiz" net yazılmalı).
- "deneyim_uyumu" alanında her zaman şu formatı kullan:
  "İstenen: X yıl. Adayın deneyimi: Y yıl. Fark: Z yıl. Değerlendirme: ..."

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
