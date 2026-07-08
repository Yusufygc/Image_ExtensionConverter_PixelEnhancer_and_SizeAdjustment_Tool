# Mimari

Conventor, 3 katmanlı bir masaüstü uygulaması: `core/` (iş mantığı), `ui/` (PySide6 arayüzü), `utils/` (paylaşılan yardımcılar). Katmanlar arası bağımlılık tek yönlü: `ui/` → `core/` ve `ui/` → `utils/`, ama `core/` hiçbir zaman `ui/`'a bağımlı değil.

## Katmanlar

- **`core/`** — bkz. [[core-servisleri]]. Pillow tabanlı format dönüştürme, boyutlandırma, çözünürlük artırma. Qt'den tamamen bağımsız, bu yüzden `pytest` ile UI açmadan test edilebiliyor (bkz. [[test-stratejisi]]).
- **`ui/`** — bkz. [[arayuz-katmani]]. `MainWindow`, widget'lar, `ThemeManager`, arka plan işlem thread'i.
- **`utils/`** — `path_helper.py` (Nuitka/PyInstaller uyumlu kaynak yolu çözümleme + `get_icon()`), `image_loader.py` (Pillow→QImage fallback), `constants.py` (`AppConstants`, `AppIcons`), `strings.py` (`UIStrings` — bkz. [[merkezi-icon-ve-string-yapisi]]), `logger.py`.

## Thread modeli

Ağır iş (dönüştürme/boyutlandırma/artırma) UI thread'ini kilitlememesi için `ui/worker.py`'deki `ProcessingWorker` (QThread alt sınıfı) üzerinde çalışır. `WorkerSignals` (progress/result/error/finished) ile `MainWindow`'a haber verir. `ProcessingWorker.errors` listesi her dosyanın hatasını biriktirir; `MainWindow.processing_finished()` bu listeye bakıp kısmi hata durumunda "Başarılı" değil "Kısmi Hata" diyaloğu gösterir — toplu işlemde sessiz veri kaybını önlemek için eklendi.

Pencere kapanırken (`MainWindow.closeEvent`) çalışan worker varsa `stop()` + `wait(3000)` ile güvenle durdurulur; aksi halde Qt "thread destroyed while running" ile çökebilirdi.

## Operasyon seçimi: registry pattern

`MainWindow._register_operations()` üç işlemi (Format Dönüştür / Yeniden Boyutlandırma / Kalite Artır) tek bir `self.operations` listesinde (`label`, `service`, `widget`, `collect_kwargs`) topluyor. Combo box doldurma, panel görünürlüğü (`update_options_ui`) ve `start_processing()` hepsi bu listeye bakıyor. Yeni bir operasyon eklemek tek bir kayıt eklemek demek — eskiden 3 ayrı yerde paralel `if/elif` zinciri vardı (Shotgun Surgery), artık yok.

## Stil sistemi

`assets/style/main.qss` merkezi QSS dosyası, widget'lar `setObjectName(...)` ile QSS seçicilerine bağlanıyor (örn. `QPushButton#IconOnlyButton`, `QFrame#DropZone`). Python tarafında inline `setStyleSheet()` çağrısı yok — hepsi kaldırıldı, bkz. [[arayuz-katmani]]. Sürükle-bırak sırasındaki dinamik "aktif" durumu `self.setProperty("dragActive", ...)` + `style().polish()` ile QSS'e yansıtılıyor (Qt dynamic property selector deseni), inline renk kodu yok.

İlgili: [[teknoloji-yigini]], [[build-ve-dagitim]], [[RULES]]
