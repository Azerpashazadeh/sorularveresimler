import os
import json
import time

# Dosyanın tam yolu (Test 8 için)
yol = r"C:\Users\matht\sorularveresimler\test8\arabicjsons\test8-radioar.json"

print(f"--- TEST 8 DENETİMİ BAŞLADI ---")

if os.path.exists(yol):
    # 1. Dosyanın şu anki (eski) durumunu al
    eski_zaman = os.path.getmtime(yol)
    eski_boyut = os.path.getsize(yol)
    
    with open(yol, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. Metni "DEDEKTIF TESTI" olarak damgalayalım
    test_metni = f"DEDEKTIF TESTI - SAAT: {time.strftime('%H:%M:%S')}"
    data['sorular'][0]['soru'] = test_metni
    
    # 3. Üzerine yaz
    with open(yol, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # 4. Yazdıktan sonraki durumu kontrol et
    time.sleep(1) # Windows'un dosyayı işlemesi için 1 saniye bekle
    yeni_zaman = os.path.getmtime(yol)
    yeni_boyut = os.path.getsize(yol)
    
    print(f"📁 Dosya: {yol}")
    print(f"🕒 Eski Değişim: {time.ctime(eski_zaman)}")
    print(f"🕒 Yeni Değişim: {time.ctime(yeni_zaman)}")
    
    if yeni_zaman > eski_zaman:
        print("\n✅ WINDOWS ONAYI: Dosya sistemi 'Bu dosya az önce değişti' diyor.")
        print(f"📝 Yazılan Metin: {test_metni}")
        print("\n👉 ŞİMDİ YAPMAN GEREKEN: Bu dosyayı NOT DEFTERİ ile aç ve ilk soruya bak.")
    else:
        print("\n❌ HATA: Dosya tarihi değişmedi! Windows yazma işlemini engelliyor olabilir.")
else:
    print(f"❌ DOSYA BULUNAMADI: {yol} yolunu kontrol et.")