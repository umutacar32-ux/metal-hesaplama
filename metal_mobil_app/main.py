import streamlit as st
import math

# Sayfa Ayarları (Telefon Ekranı Düzeni)
st.set_page_config(page_title="Metal Ağırlık Hesapla", page_icon="📲", layout="centered")

# Şık Mobil Koyu Tema Tasarımı (CSS)
st.markdown("""
    <style>
    .main { background-color: #1E1E24; }
    /* Hesapla Butonu */
    div.stButton > button:first-child {
        background-color: #00ADB5 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        height: 2.8em !important;
        width: 100% !important;
        border-radius: 12px !important;
        border: none !important;
    }
    /* Sonuç Kartı */
    .sonuc-kutusu {
        background-color: #393E46;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border-left: 5px solid #00ADB5;
        margin-bottom: 20px;
    }
    /* Hak Gösterge Paneli */
    .hak-paneli {
        background-color: #222831;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Cad Cam Sektörü sitesindeki tüm standart malzeme yoğunlukları (g/cm³)
MATERIAL_DENSITIES = {
    "demir": 7.86, "celik": 7.85, "paslanmaz_celik": 7.95, "aluminyum": 2.72,
    "bakir": 8.96, "bronz": 8.80, "pirinc": 8.50, "titanyum": 4.54,
    "kursun": 11.34, "cinko": 7.14, "plastik_delrin": 1.42, "kestamid": 1.15, "poliamid": 1.14
}

# 📱 TELEFON HAFIZASI
if "kalan_hak" not in st.session_state:
    st.session_state.kalan_hak = 3

st.title("📲 Metal Hesaplama Pro")
st.write("Google Play & App Store Mobil Sürüm Prototipi")

# 🔋 Hak Gösterge Kartı
hak_rengi = "#00ADB5" if st.session_state.kalan_hak > 0 else "#FF2E93"
st.markdown(f"""
    <div class="hak-paneli" style="border: 1px solid {hak_rengi};">
        <span style="color: #888888; font-size: 14px;">Kalan Ücretsiz İşlem Hakkınız: </span>
        <span style="color: {hak_rengi}; font-size: 18px;">{st.session_state.kalan_hak}</span>
    </div>
""", unsafe_allow_html=True)

# 1. Profil ve Malzeme Seçimleri
profil_tipi = st.selectbox("Profil Tipi Seçin", ["mil", "boru", "sac", "kare", "profil", "altikose"])
malzeme = st.selectbox("Malzeme Tipi Seçin", list(MATERIAL_DENSITIES.keys()))

st.write("---")

# 2. Dinamik Girdi Alanları
cap, et_kalinligi, kalinlik, genislik, boy, kenar = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

if profil_tipi in ["mil", "boru"]:
    cap = st.number_input("Çap (mm)", min_value=0.0, value=50.0)
if profil_tipi == "boru":
    et_kalinligi = st.number_input("Et Kalınlığı (mm)", min_value=0.0, value=2.0)
if profil_tipi in ["sac", "lama"]:
    kalinlik = st.number_input("Kalınlık (mm)", min_value=0.0, value=5.0)
    genislik = st.number_input("Genişlik (mm)", min_value=0.0, value=100.0)
if profil_tipi == "profil":
    genislik = st.number_input("Genişlik (mm)", min_value=0.0, value=40.0)
    boy = st.number_input("Boy / Yükseklik (mm)", min_value=0.0, value=40.0)
    et_kalinligi = st.number_input("Et Kalınlığı (mm)", min_value=0.0, value=2.0)
if profil_tipi in ["kare", "altikose"]:
    kenar = st.number_input("Kenar / Anahtar Ağzı Ölçüsü (mm)", min_value=0.0, value=20.0)

uzunluk = st.number_input("Toplam Uzunluk (mm)", min_value=0.0, value=1000.0)
adet = st.number_input("Adet", min_value=1, value=1)

st.write("")

# 3. 🎯 GEÇERLİ HESAPLAMA MOTORU VE REKLAM MANTIĞI
if st.session_state.kalan_hak > 0:
    if st.button("HESAPLA"):
        st.session_state.kalan_hak -= 1
        
        # Formülleri doğrudan içeride çalıştırıyoruz (İnternet ihtiyacı sıfırlandı!)
        yogunluk = MATERIAL_DENSITIES[malzeme]
        hacim_mm3 = 0.0
        
        if profil_tipi == "mil":
            r = cap / 2
            hacim_mm3 = math.pi * (r ** 2) * uzunluk
        elif profil_tipi == "boru":
            r_dis = cap / 2
            r_ic = r_dis - et_kalinligi
            hacim_mm3 = math.pi * ((r_dis ** 2) - (r_ic ** 2)) * uzunluk
        elif profil_tipi in ["sac", "lama"]:
            hacim_mm3 = kalinlik * genislik * uzunluk
        elif profil_tipi == "kare":
            hacim_mm3 = (kenar ** 2) * uzunluk
        elif profil_tipi == "profil":
            boy_olcusu = boy if boy > 0 else genislik
            dis_alan = genislik * boy_olcusu
            ic_genislik = genislik - (2 * et_kalinligi)
            ic_boy = boy_olcusu - (2 * et_kalinligi)
            hacim_mm3 = (dis_alan - (ic_genislik * ic_boy)) * uzunluk
        elif profil_tipi == "altikose":
            hacim_mm3 = ((3 * math.sqrt(3)) / 2) * ((kenar / math.sqrt(3)) ** 2) * uzunluk

        # Ağırlık hesaplama
        hacim_cm3 = hacim_mm3 / 1000.0
        toplam_agirlik_kg = (hacim_cm3 * yogunluk * int(adet)) / 1000.0
        agirlik_sonuc = round(toplam_agirlik_kg, 3)
        
        # Sonucu ekranda saklamak için session state kullanıyoruz
        st.session_state.son_sonuc = agirlik_sonuc
        st.rerun()

    # Eğer hesaplanmış bir sonuç varsa ekranda göster
    if "son_sonuc" in st.session_state:
        st.markdown(f"""
            <div class="sonuc-kutusu">
                <h3 style='color: #888888; margin:0; font-size:13px; letter-spacing:1px;'>TOPLAM AĞIRLIK</h3>
                <h1 style='color: #00ADB5; margin:10px 0 0 0; font-size:42px;'>{st.session_state.son_sonuc} kg</h1>
            </div>
        """, unsafe_allow_html=True)

else:
    st.error("Günlük ücretsiz işlem hakkınız bitmiştir!")
    st.markdown("""
        <style>
        div.stButton > button:first-child { background-color: #FF2E93 !important; animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("🎬 REKLAM İZLE (+10 HAK KAZAN)"):
        with st.spinner("Reklam yükleniyor (10 Saniye)..."):
            import time
            time.sleep(3)
        
        st.session_state.kalan_hak = 10
        if "son_sonuc" in st.session_state:
            del st.session_state.son_sonuc # Yeni hak gelince eski sonucu temizler
        st.success("Tebrikler! Reklamı başarıyla izlediniz. Hesabınıza +10 Hak eklendi!")
        st.rerun()
