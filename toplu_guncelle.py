import json
import os

def linkleri_enjekte_et(kaynak_veriler, hedef_veriler):
    """İngilizce verideki linkleri hedef veriye enjekte eder."""
    eng_sorular = {s.get("numara"): s for s in kaynak_veriler.get("sorular", [])}
    
    for hedef_soru in hedef_veriler.get("sorular", []):
        numara = hedef_soru.get("numara")
        if numara in eng_sorular:
            kaynak_soru = eng_sorular[numara]
            
            # 1. Ana Medya Linkleri
            if "resim" in kaynak_soru: hedef_soru["resim"] = kaynak_soru["resim"]
            if "video" in kaynak_soru: hedef_soru["video"] = kaynak_soru["video"]
            
            # 2. Seçeneklerdeki Linkler
            if "secenekler" in kaynak_soru:
                hedef_soru["secenekler"] = kaynak_soru["secenekler"]
            
            # 3. Doğru Cevap Link Listesi
            if "dogruCevap" in kaynak_soru and isinstance(kaynak_soru["dogruCevap"], list):
                hedef_soru["dogruCevap"] = kaynak_soru["dogruCevap"]

            # 4. Drag-Drop Elemanları
            if "elements" in kaynak_soru:
                hedef_soru["elements"] = kaynak_soru["elements"]

            # 5. Feedback Linkleri
            if "feedback" in kaynak_soru and "feedback" in hedef_soru:
                f = kaynak_soru["feedback"]
                hedef_soru["feedback"]["dogruCevapResim"] = f.get("dogruCevapResim")
                hedef_soru["feedback"]["yanlisCevapResim"] = f.get("yanlisCevapResim")
                hedef_soru["feedback"]["cevaplanmamisResim"] = f.get("cevaplanmamisResim")
    
    return hedef_veriler

# --- GÜNCELLEDİĞİMİZ KISIM BURASI ---
klasor_araligi = range(7, 51) # 7'den başlar, 51'e kadar (50 dahil) gider
# -----------------------------------

dosya_tipleri = ["radio", "fillblank", "checkbox", "dragdrop"]
diller = {"arabicjsons": "ar", "dutchjsons": "nl", "turkishjsons": "tr"}

for i in klasor_araligi:
    ana_klasor = f"test{i}"
    if not os.path.exists(ana_klasor):
        print(f"Atlanıyor: {ana_klasor} henüz mevcut değil.")
        continue

    print(f"--- İşleniyor: {ana_klasor} ---")

    for tip in dosya_tipleri:
        eng_dosya_yolu = os.path.join(ana_klasor, "englishjsons", f"{ana_klasor}-{tip}en.json")
        
        if not os.path.exists(eng_dosya_yolu):
            continue

        with open(eng_dosya_yolu, 'r', encoding='utf-8') as f:
            eng_data = json.load(f)

        for klasor_adi, dil_kodu in diller.items():
            hedef_dosya_yolu = os.path.join(ana_klasor, klasor_adi, f"{ana_klasor}-{tip}{dil_kodu}.json")
            
            if os.path.exists(hedef_dosya_yolu):
                with open(hedef_dosya_yolu, 'r', encoding='utf-8') as f:
                    hedef_data = json.load(f)

                guncel_data = linkleri_enjekte_et(eng_data, hedef_data)

                with open(hedef_dosya_yolu, 'w', encoding='utf-8') as f:
                    json.dump(guncel_data, f, ensure_ascii=False, indent=4)
                print(f"  Güncellendi: {hedef_dosya_yolu}")

print("İşlem tamamlandı!")
