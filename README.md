# Conventor - Gelişmiş Resim Dönüştürücü ve İyileştirici

**Conventor**, modern arayüzü ve güçlü alt yapısı ile resim dosyalarınızı hızlıca dönüştürmenizi, boyutlandırmanızı ve kalitesini artırmanızı sağlayan bir masaüstü uygulamasıdır. PySide6 ve Pillow kütüphaneleri kullanılarak geliştirilmiştir.

## 🚀 Özellikler

### 1. Format Dönüştürme (Converter)
Popüler resim formatları arasında hızlı ve kayıpsız dönüşüm sağlar.
*   **Desteklenen Formatlar:** JPEG, PNG, WEBP, BMP, ICO, TIFF, SVG.
*   **ICO Desteği:** 256px, 128px, 64px, 32px, 16px boyutlarını içeren çok katmanlı ICO dosyaları oluşturur.
*   **SVG Desteği:** Raster görselleri (PNG/JPG) SVG içerisine gömerek vektörel formatta saklar.

### 2. Yeniden Boyutlandırma (Resizer)
Görsellerinizin boyutlarını ihtiyacınıza göre ayarlayın.
*   **Piksel Bazlı:** Genişlik ve yükseklik değerlerini elle girerek kesin boyutlandırma.
*   **Yüzde Bazlı:** Orijinal boyuta göre %1 ile %500 arasında ölçeklendirme.

### 3. Kalite ve Çözünürlük Artırma (Enhancer)
Düşük çözünürlüklü görselleri yapay zeka benzeri yöntemlerle iyileştirir.
*   **Akıllı Ölçekleme:** LANCZOS algoritması ile yüksek kaliteli upscaling (büyütme).
*   **Keskinleştirme:** *Unsharp Mask* filtresi ile detayları belirginleştirme.
*   **Kontrast Ayarı:** Görüntüye canlılık katan otomatik kontrast optimizasyonu.
*   **Destek:** 1.1x ile 4.0x kat arasında büyütme ve iyileştirme.

### 4. Kullanıcı Dostu Arayüz
*   **Sürükle & Bırak:** Dosyalarınızı uygulama üzerine sürükleyerek hızlıca listeye ekleyin.
*   **Karanlık Mod (Dark Mode):** Göz yormayan, modern ve şık tasarım (`#1e1e2e` tabanlı).
*   **Toplu İşlem:** Birden fazla dosyayı aynı anda işleyin.
*   **İlerleme Takibi:** İşlem durumunu anlık gösteren ilerleme çubuğu.

## 🛠️ Kurulum ve Çalıştırma

### 1. Kolay Kurulum (Önerilen)
Uygulamayı herhangi bir Python kurulumuna ihtiyaç duymadan, doğrudan Setup Wizard aracılığıyla kurabilirsiniz.

1.  **`ConverterApp.exe`** dosyasını çalıştırın.
2.  Açılan kurulum sihirbazındaki (Setup Wizard) adımları takip edin.
3.  Kurulum tamamlandığında masaüstündeki kısayol veya başlat menüsü üzerinden programı hemen kullanmaya başlayabilirsiniz.

### 2. Geliştirici Kurulumu (Manuel)
Eğer kaynak kod üzerinden çalışmak veya geliştirme yapmak istiyorsanız:

1.  **Gereksinimleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Uygulamayı Başlatın:**
    ```bash
    python main.py
    ```

## 📦 Kaynak Koddan Modüler EXE Oluşturma (Build)

Uygulamayı kendiniz derlemek isterseniz **Nuitka** kullanabilirsiniz:

1.  `build.bat` dosyasını çalıştırın.
2.  İşlem bittiğinde `dist/main.exe` dosyası oluşturulacaktır.

**Not:** Derleme işlemi sırasında `assets`, `core`, `ui` gibi gerekli modüller ve veri dosyaları exe içerisine gömülür.

## 📂 Proje Yapısı

```
Converter/
├── assets/             # İkonlar ve görsel kaynaklar
├── core/               # İş mantığı katmanı
│   ├── converter.py    # Dönüştürme işlemleri
│   ├── enhancer.py     # İyileştirme işlemleri
│   ├── resizer.py      # Boyutlandırma işlemleri
│   └── interfaces.py   # Soyut sınıflar
├── ui/                 # Arayüz katmanı (PySide6)
│   ├── widgets/        # Özelleştirilmiş widgetlar (DropZone vb.)
│   ├── views/          # Sayfa görünümleri
│   ├── styles/         # Tema ve stil dosyaları
│   ├── main_window.py  # Ana pencere
│   └── worker.py       # Arka plan işlemleri (Thread)
├── utils/              # Yardımcı araçlar
├── main.py             # Uygulama giriş noktası
├── build.bat           # Nuitka derleme scripti
└── requirements.txt    # Python bağımlılıkları
```

## 📝 Lisans

Bu proje açık kaynaklıdır ve kişisel kullanım için serbesttir.
