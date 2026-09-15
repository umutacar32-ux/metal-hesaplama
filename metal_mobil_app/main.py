import streamlit as st
import time

# Eğer projenizde custom fonksiyonlar varsa onların hata vermemesi için importlar
try:
    import constants
    import interface
except ImportError:
    pass

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Metal Hesaplama",
    page_icon="⚙️",
    layout="centered"
)

# --- GOOGLE ADMOB REKLAM ALTYAPISI ---
# Not: İleride mağazaya çıkarken buradaki TEST kimliklerini gerçek AdMob kimliklerinizle değiştireceğiz.
ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713"  # Google Test App ID
ADMOB_REWARDED_ID = "ca-app-pub-3940256099942544/5224354917"  # Google Test Ödüllü Reklam ID

# Session State (Hak Takibi) Başlatma
if "kalan_hak" not in st.session_state:
    st.session_state.kalan_hak = 3  # Günlük 3 ücretsiz hak

# Uygulama Başlığı
st.title("⚙️ Metal Hesaplama Uygulaması")
st.write(f"📊 **Kalan Ücretsiz İşlem Hakkınız:** `{st.session_state.kalan_hak}`")

# --- HAK KONTROLÜ VE UYGULAMA MANTIĞI ---
if st.session_state.kalan_hak > 0:
    st.info("Hesaplama formunuz aşağıdadır. Her hesaplama işleminde 1 hakkınız düşer.")
    
    # Örnek Hesaplama Butonu (Sizin kendi hesaplama formunuz buraya gelecek)
    if st.button("🧮 Hesapla"):
        with st.spinner("Hesaplanıyor..."):
            time.sleep(1)
        st.session_state.kalan_hak -= 1
        st.session_state.son_sonuc = "Hesaplama Başarıyla Tamamlandı!"
        st.success(st.session_state.son_sonuc)
        st.rerun()

else:
    st.warning("⚠️ Günlük ücretsiz işlem hakkınız bitmiştir! Devam etmek için reklam izleyerek +10 hak kazanabilirsiniz.")

st.write("---")

# --- REKLAM İZLEME VE ÖDÜL BUTONU ---
# CSS ile butonun nabız gibi büyümesini sağlayan görsel efekt (Fotoğrafınızdaki stil)
st.markdown(
    """
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    div.stButton > button:first-child {
        animation: pulse 2s infinite;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("🎬 REKLAM İZLE (+10 HAK KAZAN)"):
    with st.spinner("Reklam yükleniyor... (10 Saniye)"):
        # İleride iPhone uygulaması içine gömdüğümüzde gerçek AdMob reklamını tetikleyecek görünmez JavaScript kodu
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
        
    # Ödül tanımlama işlemleri
    st.session_state.kalan_hak += 10
    if "son_sonuc" in st.session_state:
        del st.session_state.son_sonuc  # Eski sonucu temizle
        
    st.success("🎉 Tebrikler! Reklamı başarıyla izlediniz. Hesabınıza +10 Hak Eklendi!")
    time.sleep(1)
    st.rerun()
