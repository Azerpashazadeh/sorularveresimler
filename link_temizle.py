import os
import json
import re

def bosluklari_temizle():
    # test1'den test50'ye kadar tüm klasörleri tara
    for i in range(1, 51):
        ana_klasor = f"test{i}"
        if not os.path.exists(ana_klasor):
            continue

        print(f"--- Temizlik Başladı: {ana_klasor} ---")

        # Klasörün içindeki tüm alt klasörleri ve dosyaları gez
        for root, dirs, files in os.walk(ana_klasor):
            for file in files:
                if file.endswith(".json"):
                    dosya_yolu = os.path.join(root, file)
                    
                    with open(dosya_yolu, 'r', encoding='utf-8') as f:
                        icerik = f.read()

                    # MP4 linklerindeki "/ 2.mp4" gibi boşlukları bul ve "/" ile birleştir
                    # Regex açıklaması: / işaretinden sonra gelen bir veya daha fazla boşluğu bulur
                    yeni_icerik = re.sub(r'/ +', '/', icerik)

                    if icerik != yeni_icerik:
                        with open(dosya_yolu, 'w', encoding='utf-8') as f:
                            f.write(yeni_icerik)
                        print(f"  [DÜZELTİLDİ] {dosya_yolu}")

if __name__ == "__main__":
    bosluklari_temizle()
    print("Tüm dosyalardaki link boşlukları temizlendi!")
