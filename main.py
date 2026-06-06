from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# ============ AGENTS ============

cv_analyst = Agent(
    role="Senior Technical Recruiter & CV Analysis Specialist",
    goal="""Yazılım mühendisliği CV'lerini analiz ederek adayın teknik becerilerini, 
    deneyim derinliğini, eğitim geçmişini ve proje portföyünü yapılandırılmış 
    ve eksiksiz biçimde dokümante etmek.""",
    backstory="""Yazılım sektöründe 12 yıldır teknik işe alım süreçlerinde yer alıyorsun. 
    Google, Microsoft gibi büyük teknoloji şirketlerinde ve erken aşama startuplarda 
    500'den fazla yazılım mühendisini işe aldın. Python, ML, backend ve frontend 
    pozisyonlarında uzmanlaştın. Bir CV'ye bakarak adayın gerçek yetkinlik seviyesini, 
    proje kalitesini ve kariyer gelişimini saniyeler içinde çıkarabiliyorsun.""",
    verbose=True,
)

job_analyst = Agent(
    role="Senior Job Market Analyst & Technical Requirements Specialist",
    goal="""Yazılım mühendisliği iş ilanlarını analiz ederek beklenen teknik becerileri,
    deneyim gereksinimlerini, teknoloji stack'ini ve şirket kültürünü yapılandırılmış
    ve eksiksiz biçimde dokümante etmek.""",
    backstory="""Yazılım sektöründe 12 yıldır hem işveren hem recruiter perspektifinden
    iş ilanlarını analiz ediyorsun. Google, Microsoft gibi büyük teknoloji şirketlerinde
    ve erken aşama startuplarda işe alım süreçleri tasarladın. Bir iş ilanındaki
    gerçek gereksinimleri, gizli beklentileri ve şirket kültürünü saniyeler içinde
    okuyabiliyorsun.""",
    verbose=True,
)

match_analyst = Agent(
    role="Senior CV & Job Match Specialist",
    goal="""CV analizi ve iş ilanı gereksinimlerini karşılaştırarak 
    adayın pozisyona uyumunu kapsamlı biçimde değerlendirmek.""",
    backstory="""Hem teknik recruiter hem de kariyer koçu olarak 10 yıl çalıştın.
    Yüzlerce aday-pozisyon eşleştirmesi yaptın. Bir adayın eksiklerini,
    güçlü yönlerini ve gelişim alanlarını objektif biçimde raporlayabiliyorsun.""",
    verbose=True,
)

cover_letter_writer = Agent(
    role="Senior Career Coach & Professional Cover Letter Writer",
    goal="""Aday profili ve iş ilanı gereksinimlerine göre 
    kişiselleştirilmiş, ikna edici cover letter üretmek.""",
    backstory="""10 yıldır kariyer koçluğu yapıyorsun. Yazdığın cover letter'lar
    adayların işe alınma oranını 3 katına çıkardı. Her cover letter'ı
    adayın güçlü yönlerini ön plana çıkaracak şekilde yazıyorsun.""",
    verbose=True,
)

interview_coach = Agent(
    role="Senior Technical Interview Coach",
    goal="""Aday profili ve iş ilanına göre muhtemel mülakat sorularını
    ve ideal cevap stratejilerini hazırlamak.""",
    backstory="""FAANG şirketlerinde 8 yıl teknik mülakatçı olarak çalıştın.
    Binlerce mülakat yaptın. Hangi soruların sorulacağını ve
    ideal cevapların nasıl olması gerektiğini çok iyi biliyorsun.""",
    verbose=True,
)

# ============ TASKS ============

cv_task = Task(
    description="""
    Sana verilen CV metnini dikkatle analiz et.
    CV metni: {cv_text}

    Şunları çıkar:
    - Teknik beceriler
    - Deneyim süresi ve pozisyonlar
    - Eğitim bilgileri
    - Projeler
    """,
    expected_output="""
    Aşağıdaki JSON formatında çıktı ver:
    {
        "teknik_beceriler": ["Python", "SQL", ...],
        "deneyim": [{"pozisyon": "...", "sure": "...", "sirket": "..."}],
        "egitim": {"derece": "...", "bolum": "...", "okul": "..."},
        "projeler": ["...", "..."]
    }
    """,
    agent=cv_analyst,
)

job_task = Task(
    description="""
    Sana verilen iş ilanı metnini dikkatle analiz et.
    İlan metni: {job_text}

    Şunları çıkar:
    - Zorunlu teknik beceriler
    - Tercih edilen teknik beceriler
    - Deneyim süresi ve pozisyon seviyesi
    - Şirket kültürü ve çalışma biçimi
    """,
    expected_output="""
    Aşağıdaki JSON formatında çıktı ver:
    {
        "zorunlu_beceriler": ["Python", "SQL", ...],
        "tercih_edilen": ["Docker", "Kubernetes", ...],
        "deneyim": [{"pozisyon": "...", "sure": "..."}],
        "sirket_kulturu": ["...", "..."]
    }
    """,
    agent=job_analyst,
)

match_task = Task(
    description="""
    CV analiz sonucu ve iş ilanı analiz sonucunu karşılaştır.

    Şunları değerlendir:
    - Eşleşen teknik beceriler
    - Eksik beceriler
    - Deneyim uyumu
    - Genel uyum puanı (0-100)
    """,
    expected_output="""
    {
        "uyum_puani": 85,
        "eslesen_beceriler": ["Python", "SQL", ...],
        "eksik_beceriler": ["Kubernetes", ...],
        "deneyim_uyumu": "...",
        "genel_degerlendirme": "..."
    }
    """,
    agent=match_analyst,
    context=[cv_task, job_task],
)

cover_letter_task = Task(
    description="""
    CV analizi ve uyum analizi sonuçlarına göre kişiselleştirilmiş cover letter yaz.

    - Güçlü yönleri ön plana çıkar
    - Eksikleri fırsata çevir
    - Profesyonel ve ikna edici bir dil kullan
    """,
    expected_output="""
    Profesyonel, 3 paragraftan oluşan cover letter metni.
    Paragraf 1: Güçlü giriş ve pozisyona ilgi
    Paragraf 2: Eşleşen beceriler ve deneyimler
    Paragraf 3: Motivasyon ve kapanış
    """,
    agent=cover_letter_writer,
    context=[cv_task, job_task, match_task],
)

interview_task = Task(
    description="""
    Aday profili ve iş ilanına göre mülakat soruları hazırla.

    - Teknik sorular
    - Davranışsal sorular
    - Her soru için ideal cevap stratejisi
    """,
    expected_output="""
    {
        "teknik_sorular": [
            {"soru": "...", "ideal_cevap_stratejisi": "..."}
        ],
        "davranissal_sorular": [
            {"soru": "...", "ideal_cevap_stratejisi": "..."}
        ]
    }
    """,
    agent=interview_coach,
    context=[cv_task, job_task, match_task],
)

# ============ CREW ============

crew = Crew(
    agents=[
        cv_analyst,
        job_analyst,
        match_analyst,
        cover_letter_writer,
        interview_coach,
    ],
    tasks=[cv_task, job_task, match_task, cover_letter_task, interview_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff(
    inputs={
        "cv_text": "Ahmet Yılmaz, 3 yıl Python geliştirici, Django, PostgreSQL, Git biliyor. Bilgisayar Mühendisliği mezunu.",
        "job_text": "Backend Developer aranıyor. Python, Django, Docker, AWS bilgisi şart. 3+ yıl deneyim.",
    }
)

cv_output = cv_task.output.raw
job_output = job_task.output.raw
match_output = match_task.output.raw
cover_letter = cover_letter_task.output.raw
interview_output = interview_task.output.raw

print(result)
