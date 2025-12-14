# Görev Planı: SAP B1 Video Destekli Dokümantasyon Otomasyonu (Jules)

Bu plan, SAP B1 Add-on eğitim videolarından **AIFTeam Kurumsal Standartlarına** tam uyumlu kullanıcı dokümanları üretmek amacıyla hazırlanmıştır.

## 1. Proje Analizi ve Hedef

**Mevcut Durum:**
- Kaynak: Eğitim videoları (.mp4) ve ham transkriptler (.vtt).
- Hedef: `Çoklu Para Birimi Sihirbazı Kullanıcı Dokümanı.docx` formatında, profesyonel Word dokümanı.
- Kritik İhtiyaç: Videodaki anlatım ile ekrandaki görselin senkronize edilmesi ve görsel üzerinde odak noktalarının (mümkünse) belirtilmesi.

## 2. Referans Doküman Standartları (Style Guide)

`Çoklu Para Birimi Sihirbazı Kullanıcı Dokümanı.docx` analizine göre uyulması gereken kurallar:

### 2.1. Görsel Yapı
- **Kapak:** AIFTeam Logosu, Doküman Adı, Versiyon Bilgisi.
- **Font:** Kurumsal font (Genelde Calibri veya Arial, 11pt).
- **Başlıklar:** Hiyerarşik ve numaralı (1. Giriş, 2. Kurulum, 2.1. Ayarlar).

### 2.2. İçerik Akışı
1.  **Amaç & Kapsam:** Dokümanın neden yazıldığı.
2.  **Ön Hazırlık:** Add-on çalıştırma adımları.
3.  **Süreç Adımları (Ana Gövde):**
    - "Adım X: [İşlem Adı]" formatı.
    - Ekran görüntüsü.
    - Görüntü altında açıklayıcı metin (Örn: "Şekil 1'de görüldüğü gibi...").
4.  **Uyarılar:** "Dikkat Edilmesi Gerekenler" bölümü.
5.  **Tarihçe & Yasal:** Versiyon tablosu ve telif hakkı metni.

### 2.3. Görsel İşleme (Zorluk Seviyesi: Yüksek)
- **Ekran Görüntüsü:** Video akışından ilgili saniyedeki kare alınmalı.
- **Kırmızı Kutu (Red Box):**
    - *Otomasyon:* OpenCV ile fare hareketi veya tıklama anı tespit edilip etrafına dikdörtgen çizilebilir.
    - *Manuel:* Otomasyon ham resmi basar, kullanıcı Word üzerinde kutuyu çizer.
    - **Karar:** İlk fazda ham resim basılacak, ancak "Highlighting" için altyapı hazırlanacak.

## 3. Teknik Yaklaşım ve İş Akışı

### Adım 1: İçerik Ayrıştırma (AI Destekli)
Transkript ham metni, doğrudan dokümana yapıştırılamaz. Konuşma dili yazı diline çevrilmelidir.
- **Girdi:** ".vtt" dosyası.
- **İşlem:** AI Modeli (Gemini/GPT) kullanılarak konuşma metni "Talimat" formatına çevrilir. ( örn: "Buraya basıyoruz" -> "Kaydet butonuna basınız" ).
- **Çıktı:** `content_plan.json` (Zaman damgası, Düzenlenmiş Metin, Başlık Tipi).

### Adım 2: Görüntü Yakalama (Frame Extraction)
- Python (`opencv`) scripti, `content_plan.json` içindeki saniyeleri okur.
- Videodan o saniyedeki kareyi yüksek çözünürlükte `.jpg` olarak kaydeder.
- (Opsiyonel) Görüntü tekrarı kontrolü yapılır (Sahne değişmediyse yeni resim alma).

### Adım 3: Doküman Montajı (Assembler)
- `python-docx` kütüphanesi kullanılır.
- Şablon (`template.docx`) varsa ona sadık kalır, yoksa sıfırdan oluşturur.
- Metin -> Resim -> Resim Altyazısı döngüsüyle saylalar oluşturulur.
- Otomatik "İçindekiler" ve "Tarihçe" tablosu eklenir.

## 4. Geliştirme Fazları (Timeline)

### Faz 1: Omurga Kurulumu (Tamamlandı/Mevcut)
- [x] Video ve Transkript okuma.
- [x] Temel Word oluşturma.
- [x] AI tarafından yapılandırılmış içerik planı oluşturma.

### Faz 2: Görsel Zenginleştirme (Sıradaki Hedef)
- [ ] Referans dokümandaki stilin (Header/Footer, Tablo Stilleri) birebir kopyalanması.
- [ ] Kırmızı Kutu için yarı-otomatik çözüm (Örn: Mouse tıklama koordinatlarını videodan analiz etme).
- [ ] Doküman Tarihçesi tablosunun otomatik doldurulması.

### Faz 3: Kullanıcı Arayüzü (Opsiyonel)
- [ ] Komut satırı yerine basit bir arayüz (GUI) ile dosya seçimi.

## 5. Jules İçin Aksiyon Maddeleri

1.  **Mevcut Scripti İncele:** GitHub'daki `auto_doc_tool` reposunu çek ve `assembler.py` yapısını anla.
2.  **Referans Stili Kopyala:** `python-docx` kodunda, referans dokümandaki paragraf boşluklarını, font tiplerini ve başlık renklerini hard-code olarak tanımla.
3.  **Kırmızı Kutu Ar-Ge:** `opencv` ile "mouse click detection" araştırması yap. Eğer zorsa, resimlerin altına manuel düzenleme için not düşen bir yapı kur.
