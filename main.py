import math
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Geçici yoğunluk sözlüğü (constants.py yoksa hata vermemesi için)
MATERIAL_DENSITIES = {
    "demir": 7.86,
    "paslanmaz_celik": 7.95,
    "bakir": 8.96,
    "aluminyum": 2.72,
    "bronz": 8.8,
    "titanyum": 4.6
}

app = FastAPI(title="Metal Ağırlık Hesaplama API'si")

class WeightCalculationRequest(BaseModel):
    profil_tipi: str
    malzeme: str
    adet: int = 1
    cap: Optional[float] = None
    uzunluk: Optional[float] = None
    et_kalinligi: Optional[float] = None
    genislik: Optional[float] = None
    kalinlik: Optional[float] = None
    kenar: Optional[float] = None

@app.post("/hesapla")
def hesapla_metal_agirlik(req: WeightCalculationRequest):
    malzeme_key = req.malzeme.lower().strip()
    
    if malzeme_key not in MATERIAL_DENSITIES:
        raise HTTPException(status_code=400, detail="Geçersiz malzeme tipi.")
    
    yogunluk = MATERIAL_DENSITIES[malzeme_key]
    sonuc_agirlik = 0.0
    
    if req.profil_tipi.lower() == "mil":
        if not req.cap or not req.uzunluk:
            raise HTTPException(status_code=400, detail="Mil için çap ve uzunluk zorunludur.")
        yari_cap = req.cap / 2
        hacim = (yari_cap ** 2) * math.pi * req.uzunluk
        sonuc_agirlik = (hacim * yogunluk * req.adet) / 1000000

    return {
        "durum": "basarili", 
        "malzeme": req.malzeme, 
        "profil_tipi": req.profil_tipi,
        "yogunluk": yogunluk,
        "toplam_agirlik_kg": round(sonuc_agirlik, 3)
    }
