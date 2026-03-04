import json
import os
import pandas as pd

# Ana dizin
base_path = r"C:\Users\matht\sorularveresimler"
diller_bilgi = [
    {"ad": "EN", "klasor": "englishjsons", "kod": "en"},
    {"ad": "TR", "klasor": "turkishjsons", "kod": "tr"},
    {"ad": "NL", "klasor": "dutchjsons", "kod": "nl"},
    {"ad": "AR", "klasor": "arabicjsons", "kod": "ar"}
]

def dosya_icerik_getir(test_yolu, klasor_adi, tip):
    """Klasör içinde ilgili tipi içeren herhangi bir JSON dosyasını okur."""
    hedef_klasor = os.path.join(test_yolu, klasor_adi)
    if not os.path.exists(hedef_klasor):
        return None
    
    for f in os.listdir(hedef_klasor):
        f_lower = f.lower()
        # Hem 'resimsech' hem 'resimdensech' kontrolü için 'resim' kelimesi yeterli
        arama_tipi = "resim" if "resim" in tip else tip
        if arama_tipi in f_lower and f_lower.endswith('.json'):
            try:
                with open(os.path.join(hedef_klasor, f), 'r', encoding='utf-8') as j:
                    return json.load(j)
            except:
                return None
    return None

master_veriler = []
print("🔍 Master Tablo oluşturuluyor (DragDrop ve ResimSeç cevapları temizleniyor)...")

for t in range(1, 51):
    test_adi = f"test{t}"
    test_yolu = os.path.join(base_path, test_adi)
    if not os.path.exists(test_yolu): continue

    # Sabit tipler üzerinden dönelim
    for tip in ["radio", "checkbox", "fillblank", "dragdrop", "resimsech"]:
        en_data = dosya_icerik_getir(test_yolu, "englishjsons", tip)
        if not en_data: continue

        for idx, soru_en in enumerate(en_data.get('sorular', [])):
            row = {
                "Test": test_adi,
                "Tip": tip,
                "No": soru_en.get('numara', idx + 1)
            }

            for dil in diller_bilgi:
                data = dosya_icerik_getir(test_yolu, dil["klasor"], tip)
                prefix = dil["ad"]
                
                if data and idx < len(data.get('sorular', [])):
                    s = data['sorular'][idx]
                    row[f"{prefix}_Soru"] = s.get('soru', '')
                    
                    # Seçenekler (URL içerenler hariç)
                    sec = s.get('cevaplar') or s.get('secenekler') or []
                    row[f"{prefix}_Secenekler"] = " | ".join([str(x) for x in sec if not str(x).startswith('http')])
                    
                    # Feedback
                    row[f"{prefix}_Feedback"] = s.get('feedback', {}).get('metin', '')
                    
                    # DOĞRU CEVAP TEMİZLİĞİ:
                    # Dragdrop ve Resim Seçme tiplerinde cevaplar teknik veridir, Excel'de boş bırakılır.
                    if tip in ["dragdrop", "resimsech", "resimdensech"]:
                        row[f"{prefix}_DogruCevap"] = "" 
                    else:
                        dc = s.get('dogruCevap', '')
                        if isinstance(dc, list):
                            row[f"{prefix}_DogruCevap"] = ", ".join([str(x).split('/')[-1] if 'http' in str(x) else str(x) for x in dc])
                        else:
                            row[f"{prefix}_DogruCevap"] = str(dc).split('/')[-1] if 'http' in str(dc) else str(dc)
                else:
                    row[f"{prefix}_Soru"] = "[VERI_EKSIK]"

            master_veriler.append(row)

# Excel'e aktar
df = pd.DataFrame(master_veriler)
output_file = os.path.join(base_path, "MASTER_TABLO_V6_FINAL.xlsx")
df.to_excel(output_file, index=False)

print(f"\n✅ Tamamlandı! DragDrop ve Resim Seçme cevapları temizlendi.")
print(f"📁 Dosya: {output_file}")