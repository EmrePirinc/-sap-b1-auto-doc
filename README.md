# SAP B1 Video Dokümantasyon Otomasyonu

Bu proje, SAP Business One eğitim videolarını (.mp4) ve transkriptlerini (.vtt) kullanarak otomatik olarak resimli, adım adım kullanıcı kılavuzları (.docx) oluşturur.

## Özellikler

- **VTT Ayrıştırma:** Toplantı kayıtlarının altyazılarını okur ve zaman damgalarını işler.
- **Akıllı Sahne Algılama:** Sadece ekranda değişiklik olduğunda (yeni pencere, menü açılması) ekran görüntüsü alır. (Tekrar eden görüntüleri engeller).
- **Metin Temizleme (Regex):** "Arkadaşlar", "Yani" gibi dolgu kelimelerini temizler ve "Yapıyoruz" -> "Yapınız" gibi kurumsal dil dönüşümü yapar.
- **AI Destekli Montaj (Opsiyonel):** Gemini veya başka bir AI modeli tarafından oluşturulan JSON planını (`content_plan.json`) okuyup, kusursuz bir doküman montajı yapabilir (`assembler.py`).

## Dosyalar

- `doc_generator.py`: Ana araç. Regex ve görüntü işleme ile tam otomatik çalışır.
- `assembler.py`: AI destekli (Manuel Plan) çalışma için montaj scripti.
- `requirements.txt`: Gerekli kütüphaneler.

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım (Otomatik)

```bash
python doc_generator.py
```

## Kullanım (AI Planlı)

1. Bir AI modeline (GPT/Gemini) transkripti verin ve JSON formatında bir plan isteyin.
2. Planı `content_plan.json` olarak kaydedin.
3. Scripti çalıştırın:
```bash
python assembler.py
```
