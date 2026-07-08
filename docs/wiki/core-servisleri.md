# Core Servisleri

`core/` katmanı Qt'ye bağımlı değil — sadece Pillow (`PIL`) ve `utils/` kullanır. Bkz. üst bağlam: [[mimari]].

## Interface sözleşmesi

`core/interfaces.py`: `IImageProcessor` (soyut `process(image_path, **kwargs)`) → `IConverter`, `IResizer`, `IEnhancer`. Her üç servis de `process()` üzerinden tek bir giriş noktasıyla çağrılabiliyor; `ui/worker.py`'deki `ProcessingWorker` hangi somut servis olduğunu bilmeden `service.process(file_path, **kwargs)` çağırıyor (Strategy pattern'e yakın).

Tüm somut metotlar (`convert`, `resize_by_dimensions`, `resize_by_percentage`, `enhance_resolution`) opsiyonel `output_dir` parametresi alıyor — interface imzaları da bunu yansıtıyor (önceden imza uyuşmazlığı vardı, düzeltildi).

## Servisler

- **`ConverterService`** (`converter.py`) — format dönüştürme. ICO çıktısı 5 boyut (256/128/64/32/16 px) içeriyor. SVG çıktısı gerçek vektörel değil, PNG'yi base64 ile `<image>` etiketi içine gömen bir "embedding" stratejisi.
- **`ResizerService`** (`resizer.py`) — piksel bazlı veya yüzde bazlı boyutlandırma, LANCZOS resampling.
- **`EnhancerService`** (`enhancer.py`) — LANCZOS upscale + `UnsharpMask` keskinleştirme + hafif kontrast artışı. Kalite değeri `AppConstants.ENHANCED_QUALITY` (95) — dönüştürme/boyutlandırmadaki `DEFAULT_QUALITY` (90)'dan farklı, bilinçli bir seçim (artırılmış görsellerde daha yüksek kalite hedefleniyor).

## Hata yayılım kuralı

`FileNotFoundError` hiçbir zaman generic `Exception`'a sarılmadan çağırana geçer (`except FileNotFoundError: raise` bloğu her serviste var). Diğer tüm hatalar `Exception(f"... failed: {e}")` ile sarılıp yeniden fırlatılıyor. Bu ayrım önemli: `ProcessingWorker` hata tipine göre farklı davranmasa da, servisleri doğrudan çağıran kod (örn. testler) `FileNotFoundError`'ı spesifik olarak yakalayabiliyor.

## `utils/image_loader.load_image()`

Tüm servisler dosyayı doğrudan `PIL.Image.open()` yerine `utils/image_loader.load_image()` üzerinden açar. Bu fonksiyon önce Pillow'u dener, `UnidentifiedImageError` alırsa Qt'nin `QImageReader`'ına düşer (SVG ve bazı ICO'lar için Pillow desteği zayıf). Dosya var/yok kontrolü de burada tek yerde yapılıyor — servislerde ayrıca tekrarlanmıyor.

İlgili: [[test-stratejisi]] (bu servisler için pytest paketi), [[RULES]]
