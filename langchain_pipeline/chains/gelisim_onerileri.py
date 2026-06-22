from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

_ROLE = """Sen bir Senior CV Review Specialist'sin.
Yazılım sektöründe 10+ yıllık deneyimle adayların CV'lerini hedefledikleri
pozisyona göre iyileştirmelerine yardım ediyorsun. Odak noktan, adayın
CV'sinde eklemesi, güçlendirmesi veya farklı şekilde sunması gereken
içerikleri net biçimde göstermek."""

_TASK = """Aday aşağıdaki iş ilanına başvurmayı düşünüyor. Görevin, adayın
mevcut CV'sini bu pozisyona daha uygun hale getirmek için somut öneriler
vermek. Aday yeni teknoloji öğrenmiyor; mevcut bilgi ve deneyimini CV'de
daha doğru/güçlü ifade ediyor.

CV Analizi (JSON):
{cv_analysis}

İş İlanı Analizi (JSON):
{job_analysis}

Uyum Analizi (JSON):
{match_analysis}

Çıktın şu başlıkları içersin:

## Tecrübe Durumu
İlanda istenen deneyim süresi ile adayın deneyimi arasındaki farkı net yaz.
Format: "İstenen: X yıl — Sende: Y yıl". Aradaki fark CV ile kapatılamaz bir
durumsa (örn: 3+ yıl açık veya Senior pozisyona junior başvuru) bunu açıkça
belirt; teknik beceriler ne kadar güçlü olursa olsun tecrübe açığının uyum
puanını düşürdüğünü vurgula. Fark küçükse (0-1 yıl) bunu da net söyle.

## CV'ye Eklenebilecek Bilgiler
İlanda geçen ama CV'de görünmeyen, fakat adayın mevcut projeleri/deneyimi
incelendiğinde aslında sahip olduğu becerileri listele. Her madde için
"hangi proje/deneyimden çıkarılabilir" bilgisini de ver.

## Proje ve Deneyim Açıklamalarını Güçlendirme
Mevcut projelerin/iş deneyimlerinin daha iyi anlatılması için NE TÜR
detayların eklenmesi gerektiğini söyle: kullanılan teknolojiler, çözülen
problem, ölçülebilir sonuç, rol, ekip büyüklüğü vb. Bir projeyi/deneyimi
referans ver ve "burada X teknolojisini ve sağladığın katma değeri belirgin
yapmalısın" tarzında yönlendir.

## Pozisyon / Başlık Konumlandırması
Adayın CV'deki başlıkları (örn: "Yazılım Mühendisi") sektörde daha fark
edilir hale getirmek için hangi yönde konumlandırabileceğini söyle.
Konumlandırma örneği olarak somut metin/cümle yazmak yerine sektörde
tanınmış unvan/anahtar kelime örnekleri ver: "AI Strategy Expert", "LLM
Engineer", "Lead Cloud Engineer", "Senior Fullstack Developer" gibi.
Adayın hangi deneyiminin hangi konumlandırmaya zemin hazırladığını belirt.

## İlandan Eksik Anahtar Kelimeler
İlanda öne çıkan ama CV'de hiç geçmeyen anahtar kelimeleri madde madde ver
(ATS taraması için).

KESİN KURALLAR:
- Kurs, kaynak, eğitim, süre planı, 30/60/90 gün, "şu kadar ayda öğren"
  gibi öğrenme yol haritası ÖNERME.
- Adayın CV'sine kopyala-yapıştır yapacağı LİTERAL CÜMLE/İFADE YAZMA.
  "Şu cümleyi ekle: '...'", "şu ifadeyi koy: '...'" tarzı çıktılar yasak.
  Bunun yerine "ne tür bilgi eklenmeli", "hangi detay vurgulanmalı" de.
- Adayın bildiği alakalı bir teknolojiyi eksik gibi gösterme (PostgreSQL
  varsa SQL eksik değil, Spring Boot varsa Java eksik değil).

Markdown formatında, yukarıdaki başlıklarla yapılandırılmış metin döndür."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _ROLE),
        ("human", _TASK),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

gelisim_chain = prompt | llm | StrOutputParser()
