import streamlit as st
import tempfile
import os
import json
from datetime import datetime
from pipeline import run_pipeline

HISTORY_FILE = "analysis_history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(record):
    history = load_history()
    history.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def show_match(data):
    try:
        d = json.loads(data) if isinstance(data, str) else data
        st.metric("Uyum Puanı", f"{d.get('uyum_puani', '-')}/100")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Eşleşen Beceriler")
            for b in d.get("eslesen_beceriler", []):
                st.write(f"• {b}")
        with col2:
            st.subheader("❌ Eksik Beceriler")
            for b in d.get("eksik_beceriler", []):
                st.write(f"• {b}")
        st.subheader("📝 Genel Değerlendirme")
        st.write(d.get("genel_degerlendirme", ""))
    except:
        st.write(data)


def show_cover_letter(data):
    st.write(data)


def show_interview(data):
    try:
        d = json.loads(data) if isinstance(data, str) else data
        st.subheader("🔧 Teknik Sorular")
        for i, q in enumerate(d.get("teknik_sorular", []), 1):
            with st.expander(f"{i}. {q['soru']}"):
                st.write(q["ideal_cevap_stratejisi"])
        st.subheader("🤝 Davranışsal Sorular")
        for i, q in enumerate(d.get("davranissal_sorular", []), 1):
            with st.expander(f"{i}. {q['soru']}"):
                st.write(q["ideal_cevap_stratejisi"])
    except:
        st.write(data)


# ============ SAYFA YAPISI ============

st.set_page_config(
    page_title="AI Destekli İş Başvuru Asistanı", page_icon="🚀", layout="wide"
)

page = st.sidebar.radio("📌 Menü", ["🔍 Yeni Analiz", "📂 Geçmiş Analizler"])

# ============ YENİ ANALİZ ============

if page == "🔍 Yeni Analiz":
    st.title("🚀 AI Destekli İş Başvuru Asistanı")
    st.markdown("CV'nizi yükleyin, iş ilanını girin — AI sizin için analiz etsin.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 CV Yükle")
        cv_file = st.file_uploader("PDF formatında CV yükleyin", type=["pdf"])
    with col2:
        st.subheader("💼 İş İlanı")
        job_text = st.text_area("İş ilanını buraya yapıştırın", height=300)

    baslik = st.text_input(
        "📌 Bu analiz için bir başlık girin",
        placeholder="Örn: Infonal Backend Developer",
    )

    st.divider()

    if st.button("🔍 Analiz Et", type="primary", use_container_width=True):
        if not cv_file:
            st.error("Lütfen CV yükleyin.")
        elif not job_text:
            st.error("Lütfen iş ilanı girin.")
        elif not baslik:
            st.error("Lütfen bir başlık girin.")
        else:
            with st.spinner("Analiz ediliyor... 1-2 dakika sürebilir."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(cv_file.read())
                    tmp_path = tmp.name

                try:
                    result = run_pipeline(tmp_path, job_text)

                    save_history(
                        {
                            "baslik": baslik,
                            "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
                            "job_text": job_text[:200],
                            "match": result["match"],
                            "cover_letter": result["cover_letter"],
                            "interview": result["interview"],
                        }
                    )

                    st.success("Analiz tamamlandı!")
                    st.divider()

                    tab1, tab2, tab3 = st.tabs(
                        ["📊 Uyum Analizi", "✉️ Cover Letter", "🎯 Mülakat Soruları"]
                    )
                    with tab1:
                        show_match(result["match"])
                    with tab2:
                        show_cover_letter(result["cover_letter"])
                    with tab3:
                        show_interview(result["interview"])

                except Exception as e:
                    st.error(f"Hata oluştu: {str(e)}")
                finally:
                    os.remove(tmp_path)

# ============ GEÇMİŞ ANALİZLER ============

elif page == "📂 Geçmiş Analizler":
    st.title("📂 Geçmiş Analizler")
    history = load_history()

    if not history:
        st.info("Henüz kayıtlı analiz yok.")
    else:
        for i, record in enumerate(reversed(history)):
            with st.expander(f"📌 {record['baslik']} — {record['tarih']}"):
                tab1, tab2, tab3 = st.tabs(
                    ["📊 Uyum Analizi", "✉️ Cover Letter", "🎯 Mülakat Soruları"]
                )
                with tab1:
                    show_match(record["match"])
                with tab2:
                    show_cover_letter(record["cover_letter"])
                with tab3:
                    show_interview(record["interview"])
