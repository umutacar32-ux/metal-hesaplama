import streamlit as st
import time
import sys
import os

# --- KLASÖR YOLU DÜZELTMESİ ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- MODÜLLERİ ÇAĞIRMA ---
import constants
import interface

# --- IPHONE TAM EKRAN (PWA) VE MOBİL GÖRÜNÜM AYARLARI ---
st.set_page_config(
    page_title="Metal Hesaplama",
    page_icon="⚙️",
    layout="centered"
)

# iPhone'da tarayıcı çubuklarını gizleyen Apple Meta Etiketleri ve Reklam Butonu Efekti
st.markdown(
    """
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    </head>
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    /* Reklam izle butonunu özelleştirme ve hareketlendirme */
    div.stButton > button {
        animation: pulse 2s infinite !important;
        background-color: #ff4b4b !important;
        color: white !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- GOOGLE ADMOB REKLAM ALTYAPISI ---
ADMOB_REWARDED_ID = "ca-app-pub-3940256099942544/5224354917"  # Test Ödüllü Reklam ID

# Session State (Hak Takibi) Başlatma
if "kalan_hak" not in st.session_state:
    st.session_state.kalan_hak = 3  # Günlük 3 ücretsiz hak

# --- ANA BAŞLIK VE HAK GÖSTERGESİ ---
st.title("⚙️ Metal Hesaplama Uygulaması")
st.write(f"📊 **Kalan Ücretsiz İşlem Hakkınız:** `{st.session_state.kalan_hak}`")
st.write("---")

# --- ANA UYGULAMA MANTIĞI ---
if st.session_state.kalan_hak > 0:
    # Bulduğumuz asıl arayüz fonksiyonunu tetikliyoruz
    try:
        interface.profil_tipi()
    except Exception as e:
        st.error(f"Arayüz formları yüklenirken bir sorun oluştu: {e}")
            
else:
    st.warning("⚠️ Günlük ücretsiz işlem hakkınız bitmiştir! Devam etmek için aşağıdan reklam izleyerek +10 hak kazanabilirsiniz.")

st.write("---")

# --- REKLAM İZLEME VE ÖDÜL BUTONU (ALT SAYFA) ---
if st.button("🎬 REKLAM İZLE (+10 HAK KAZAN)"):
    with st.spinner("Reklam yükleniyor... (10 Saniye)"):
        st.components.v1.html(
            f"""
            <script>
                if (window.ReactNativeWebView) {{
                    window.ReactNativeWebView.postMessage(JSON.stringify({{
                        type: "SHOW_REWARDED_AD",
                        adUnitId: "{ADMOB_REWARDED_ID}"
                    }}));
                }}
            </script>
            """,
            height=0
        )
        time.sleep(10)  # Reklam izleme simülasyon süresi
        
    st.session_state.kalan_hak += 10
    st.success("🎉 Tebrikler! Reklamı başarıyla izlediniz. Hesabınıza +10 Hak Eklendi!")
    time.sleep(1)
    st.rerun()
