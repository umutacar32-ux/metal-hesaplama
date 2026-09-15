import streamlit as st
import math
import time

# --- MOBİL GÖRÜNÜM VE TAM EKRAN (PWA) AYARLARI ---
st.set_page_config(page_title="Metal Ağırlık Hesaplama", page_icon="⚙️", layout="centered")

# Şık Koyu Tema, Hesaplama Kutusu ve Nabız Efektli Reklam Butonu Tasarımı (CSS)
st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    </head>
    <style>
    .main { background-color: #1E1E24; }
    
    /* Hesapla Butonu Stili */
    div.stButton > button:first-child {
        background-color: #00ADB5 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        height: 3em !important;
        width: 100% !important;
        border-radius: 10px !important;
        border: none !important;
    }
    
    /* Sonuç Kutusu Stili */
    .sonuc-kutusu {
        background-color: #393E46;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border-left: 5px solid #00ADB5;
        margin-bottom: 25px;
    }
    
    /* Kırmızı Reklam Butonunun Nabız Gibi Büyüme Efekti */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    div.stButton > button:contains("REKLAM İZLE") {
        animation: pulse 2s infinite !important;
        background-color: #ff4b4b !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        height: 3em !important;
        width: 100% !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE ADMOB REKLAM NETWORK ID ---
ADMOB_REWARDED_ID = "ca-app-pub-3940256099942544/5224354917"  # Test Ödüllü Reklam Kimliği

# Malzeme Yoğunlukları (g/cm³)
MATERIAL_DENSITIES = {
    "demir": 7.86,
    "celik": 7.85,
    "paslanmaz_celik": 7.95,
    "aluminyum": 2.72,
    "bakir": 8.96,
    "bronz": 8.80,
    "pirinc": 8.50,
    "titanyum": 4.54,
    "kursun": 11.34,
    "cinko": 7.14,
    "plastik_delrin": 1.42,
    "kestamid": 1.15,
    "poliamid": 1.14
}

# --- HAK TAKİBİ BAŞLATMA ---
if "kalan_hak" not in st.session_state:
    st.session_state.kalan_hak = 3  # Günlük 3 ücretsiz işlem hakkı

st.title("⚙️ Metal Ağırlık Hesaplama")
st.write(f"📊 **Kalan Ücretsiz İşlem Hakkınız:** `{st.session_state.kalan_hak}`")
st.write("---")

# --- HAK VARSA FORMLARI GÖSTER ---
if st.session_state.kalan_hak > 0:
    
    # 1. Seçim Alanları
    col1, col2 = st.columns(2)
    with col1:
        profil_tipi = st.selectbox("Profil Tipi", ["mil", "boru", "sac", "kare", "profil", "altikose"])
    with col2:
        malzeme = st.selectbox("Malzeme Tipi", list(MATERIAL_DENSITIES.keys()))

    st.write("---")

    # 2. Dinamik Girdi Alanları
    cap = 0.0
    et_kalinligi = 0.0
    kalinlik = 0.0
    genislik = 0.0
    boy = 0.0
    kenar = 0.0

    if profil_tipi in ["mil", "boru"]:
        cap = st.number_input("Çap (mm)", min_value=0.0, value=50.0, step=1.0)

    if profil_tipi == "boru":
        et_kalinligi = st.number_input("Et Kalınlığı (mm)", min_value=0.0, value=2.0, step=0.5)

    if profil_tipi in ["sac", "lama"]:
        kalinlik = st.number_input("Kalınlık (mm)", min_value=0.0, value=5.0, step=0.5)
        genislik = st.number_input("Genişlik (mm)", min_value=0.0, value=100.0, step=1.0)

    if profil_tipi == "profil":
        genislik = st.number_input("Genişlik (mm)", min_value=0.0, value=40.0, step=1.0)
        boy = st.number_input("Boy / Yükseklik (mm - Kare ise boş bırakın)", min_value=0.0, value=40.0, step=1.0)
        et_kalinligi = st.number_input("Et Kalınlığı (mm)", min_value=0.0, value=2.0, step=0.5)

    if profil_tipi in ["kare", "altikose"]:
        kenar = st.number_input("Kenar / Anahtar Ağzı Ölçüsü (mm)", min_value=0.0, value=20.0, step=1.0)

    # Ortak girdiler
    uzunluk = st.number_input("Toplam Uzunluk (mm)", min_value=0.0, value=1000.0, step=10.0)
    adet = st.number_input("Adet", min_value=1, value=1, step=1)

    st.write("")

    # 3. Hesaplama Motoru
    if st.button("HESAPLA"):
        yogunluk = MATERIAL_DENSITIES[malzeme]
        hacim_mm3 = 0.0
        hata_mesaji = None

        if profil_tipi == "mil":
            if cap > 0 and uzunluk > 0:
                r = cap / 2
                hacim_mm3 = math.pi * (r ** 2) * uzunluk
            else:
                hata_mesaji = "Mil için çap ve uzunluk 0'dan büyük olmalıdır."

        elif profil_tipi == "boru":
            if cap > 0 and uzunluk > 0 and et_kalinligi > 0:
                r_dis = cap / 2
                r_ic = r_dis - et_kalinligi
                if r_ic > 0:
                    hacim_mm3 = math.pi * ((r_dis ** 2) - (r_ic ** 2)) * uzunluk
                else:
                    hata_mesaji = "Et kalınlığı dış çaptan büyük olamaz."
            else:
                hata_mesaji = "Boru için çap, et kalınlığı ve uzunluk girilmelidir."

        elif profil_tipi in ["sac", "lama"]:
            if kalinlik > 0 and genislik > 0 and uzunluk > 0:
                hacim_mm3 = kalinlik * genislik * uzunluk
            else:
                hata_mesaji = "Sac/Lama için tüm ölçüler girilmelidir."

        elif profil_tipi == "kare":
            if kenar > 0 and uzunluk > 0:
                hacim_mm3 = (kenar ** 2) * uzunluk
            else:
                hata_mesaji = "Kare malzeme için kenar ve uzunluk girilmelidir."

        elif profil_tipi == "profil":
            boy_olcusu = boy if boy > 0 else genislik
            if genislik > 0 and uzunluk > 0 and et_kalinligi > 0:
                dis_alan = genislik * boy_olcusu
                ic_genislik = genislik - (2 * et_kalinligi)
                ic_boy = boy_olcusu - (2 * et_kalinligi)
                if ic_genislik > 0 and ic_boy > 0:
                    ic_alan = ic_genislik * ic_boy
                    hacim_mm3 = (dis_alan - ic_alan) * uzunluk
                else:
                    hata_mesaji = "Et kalınlığı profil ölçülerinden büyük olamaz."
            else:
                hata_mesaji = "Profil için genişlik, et kalınlığı ve uzunluk girilmelidir."

        elif profil_tipi == "altikose":
            if kenar > 0 and uzunluk > 0:
                hacim_mm3 = ((3 * math.sqrt(3)) / 2) * ((kenar / math.sqrt(3)) ** 2) * uzunluk
            else:
                hata_mesaji = "Altıköşe için anahtar ağzı (kenar) ve uzunluk girilmelidir."

        if hata_mesaji:
            st.error(hata_mesaji)
        else:
            # Hesaplama Başarılıysa Hakkı Düşür ve Sonucu Göster
            st.session_state.kalan_hak -= 1
            hacim_cm3 = hacim_mm3 / 1000.0
            toplam_agirlik_kg = (hacim_cm3 * yogunluk * int(adet)) / 1000.0
            agirlik_sonuc = round(toplam_agirlik_kg, 3)

            st.markdown(f"""
                <div class="sonuc-kutusu">
                    <h3 style='color: #888888; margin:0; font-size:14px; letter-spacing:1px;'>HESAPLANAN TOPLAM AĞIRLIK</h3>
                    <h1 style='color: #00ADB5; margin:10px 0 0 0; font-size:48px;'>{agirlik_sonuc} kg</h1>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()

else:
    st.warning("⚠️ Günlük ücretsiz işlem hakkınız bitmiştir! Devam etmek için aşağıdan reklam izleyerek +10 hak kazanabilirsiniz.")

st.write("---")

# --- REKLAM İZLEME VE ÖDÜL ALANI ---
if st.button("🎬 REKLAM İZLE (+10 HAK KAZAN)"):
    with st.spinner("Reklam yükleniyor ve oynatılıyor... (10 Saniye)"):
        # Yarın mobil sarmalayıcıya (Wrapper) girdiğinde gerçek reklamı çağıracak JS kodu
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
        time.sleep(10)  # Reklam izleme süresi simülasyonu
        
    st.session_state.kalan_hak += 10
    st.success("🎉 Tebrikler! Reklamı başarıyla izlediniz. Hesabınıza +10 Hak Eklendi!")
    time.sleep(1)
    st.rerun()
