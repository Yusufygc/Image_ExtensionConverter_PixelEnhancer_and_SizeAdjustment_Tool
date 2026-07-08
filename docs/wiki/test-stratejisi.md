# Test Stratejisi

## Kapsam

`tests/` altında `pytest` paketi — sadece `core/` katmanını hedefliyor (bkz. [[core-servisleri]]), çünkü bu katman Qt'ye bağımlı değil ve iş mantığının tamamı burada. `ui/` katmanı (bkz. [[arayuz-katmani]]) otomatik test edilmiyor; değişikliklerden sonra `python main.py` ile elle smoke-test yapılıyor (dosya seç/sürükle, 3 operasyon, info sayfası aç/kapa, hata diyaloğu, pencere kapatma sırasında worker durdurma).

## Dosyalar

- `tests/conftest.py` — `rgba_png`, `rgb_png` fixture'ları: `tmp_path` altında Pillow ile anlık üretilen küçük test görselleri (repo'ya statik binary test verisi eklemek yerine).
- `tests/test_converter.py` — RGBA→JPEG mode dönüşümü, ICO çoklu boyut, eksik dosya → `FileNotFoundError`.
- `tests/test_resizer.py` — piksel ve yüzde bazlı boyutlandırmanın sonucu doğru boyutta mı.
- `tests/test_enhancer.py` — `factor` uygulandıktan sonra boyut doğru mu.
- `tests/test_image_loader.py` — eksik dosya, bozuk dosya, geçerli PNG.

## Çalıştırma

```
pytest tests/ -v
```
`requirements-dev.txt`'teki `pytest` ile birlikte. Venv: `venv/Scripts/python.exe -m pytest tests/`.

## Kural

`core/`'a her yeni davranış eklendiğinde (yeni format, yeni parametre, hata yolu) karşılığında bir test eklenir — bu paket olmadan `core/interfaces.py`'deki imza düzeltmesi gibi refactor'lar güvenle yapılamazdı. Bkz. [[RULES]]#kod-kuralları.

İlgili: [[mimari]], [[core-servisleri]]
