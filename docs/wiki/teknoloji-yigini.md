# Teknoloji Yığını

## Çalışma zamanı bağımlılıkları (`requirements.txt`, pinlenmiş)

- **PySide6** — arayüz (Qt6 bindings). Bkz. [[arayuz-katmani]].
- **Pillow** — görüntü işleme (`core/` katmanı). Bkz. [[core-servisleri]].

## Build bağımlılıkları (`requirements-build.txt`, ayrı — runtime'a karışmıyor)

- **Nuitka** — Python'ı native exe'ye derleyen derleyici. Bkz. [[build-ve-dagitim]].
- **zstandard** — Nuitka'nın sıkıştırma bağımlılığı.

## Geliştirme bağımlılıkları (`requirements-dev.txt`)

- **pytest** — bkz. [[test-stratejisi]].

## Logging

`utils/logger.py` → `setup_logging()`, `main.py` başında çağrılıyor. `%TEMP%/converter.log`'a yazıyor. Neden dosyaya (konsola değil): `build.bat`'taki Nuitka derlemesi `--windows-console-mode=disable` kullanıyor, yani paketlenmiş exe'de konsol yok — `print()` çıktısı hiçbir yere gitmezdi. `utils/path_helper.py` ve `ui/styles/theme.py`'deki hata/uyarı durumları `logging.exception()` / `logging.warning()` kullanıyor, `print()` değil.

## Sürüm yönetimi kuralı

`requirements.txt`'teki sürümler sabit (`==`) pinlenmiş; build-time ve dev-time bağımlılıklar ayrı dosyalarda tutulur, runtime dosyasına karıştırılmaz. Yeni bir bağımlılık eklerken bu ayrımı koru — bkz. [[RULES]]#kod-kuralları.

İlgili: [[mimari]], [[build-ve-dagitim]]
