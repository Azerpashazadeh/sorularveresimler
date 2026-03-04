import pandas as pd
import json
import os

base_path = r"C:\Users\matht\sorularveresimler"
excel_dosya_adi = "Sorular.xlsx"

def guncelle():
    excel_yolu = os.path.join(base_path, excel_dosya_adi)
    
    # DİKKAT: sheet_name=1 ekledik, bu ikinci sayfayı okur.
    # Eğer sayfanın adı özel bir isimse (Örn: "Sayfa2") sheet_name="Sayfa2" de yazabiliriz.
    df = pd.read_excel(excel_yolu, sheet_name=1) 
    
    print(f"📊 Excel'in İKİNCİ SAYFASI okundu. Satır sayısı: {len(df)}")

    basarili_soru = 0

    for index, row in df.iterrows():
        # Verileri çek
        test_adi = str(row['Test']).strip()
        tip = str(row['Tip']).strip()
        soru_no = str(row['No']).strip()
        
        yeni_soru = str(row['AR_Soru']).strip() if pd.notna(row['AR_Soru']) else None
        yeni_feedback = str(row['AR_Feedback']).strip() if pd.notna(row['AR_Feedback']) else ""

        if not yeni_soru:
            continue

        hedef_klasor = os.path.join(base_path, test_adi, "arabicjsons")
        if not os.path.exists(hedef_klasor):
            continue

        for f in os.listdir(hedef_klasor):
            if tip.lower() in f.lower() and f.endswith('.json'):
                yol = os.path.join(hedef_klasor, f)
                
                with open(yol, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                for s in data.get('sorular', []):
                    if str(s.get('numara')).strip() == soru_no:
                        # Artık ikinci sayfadaki güncel metni yazıyoruz
                        s['soru'] = yeni_soru
                        if 'feedback' in s:
                            s['feedback']['metin'] = yeni_feedback
                        break
                
                with open(yol, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                basarili_soru += 1

    print(f"\n✅ İŞLEM TAMAM: İkinci sayfadaki güncel veriler aktarıldı!")
    print(f"📝 Toplam {basarili_soru} soru güncellendi.")

if __name__ == "__main__":
    guncelle()