# Arayüz Katmanı

`ui/` PySide6 üzerine kurulu. Üst bağlam: [[mimari]].

## Dosyalar

- **`main_window.py`** — `MainWindow`. `setup_ui()` iki sayfalı bir `QStackedWidget` kurar (Ana sayfa / Bilgi sayfası). Ana sayfa kurulumu builder metotlarına bölünmüş: `_build_file_selection_group()`, `_build_operation_group()`, `_build_option_widgets()`, `_build_output_folder_selector()`, `_build_progress_section()`. Operasyon seçimi registry pattern kullanıyor (bkz. [[mimari]]#operasyon-seçimi-registry-pattern).
- **`worker.py`** — `ProcessingWorker` (QThread) + `WorkerSignals`. Bkz. [[mimari]]#thread-modeli.
- **`styles/theme.py`** — `ThemeManager`, token tabanlı dark/light tema motoru. Detay: [[tema-sistemi]].
- **`views/info_view.py`** — statik bilgi sayfası, tüm metni `UIStrings.INFO_HTML_CONTENT`'ten alıyor.
- **`widgets/drop_zone.py`** — `DropZone` (QFrame). Sürükle-bırak sırasında `AppConstants.SUPPORTED_EXTENSIONS` ile dosya uzantısı filtreleniyor; desteklenmeyen dosya bırakılırsa kısa süreli uyarı metni gösterip (`QTimer.singleShot`) varsayılan metne dönüyor.
- **`widgets/file_list_item.py`** — `FileListItemWidget`. Küçük resim önizlemesi `QImageReader.setScaledSize()` ile hedef boyutta decode ediliyor (tam çözünürlükte yükleyip küçültmek yerine — büyük dosyalarda gereksiz bellek/CPU kullanımını önlüyor).

## Merkezi ikon/string yapısı

Hiçbir dosyada `"assets/icons/..."` gibi literal path veya hardcoded Türkçe metin yok — hepsi `AppIcons` / `UIStrings` üzerinden. Detay: [[merkezi-icon-ve-string-yapisi]].

## Stil kuralı

Inline `setStyleSheet()` kullanılmıyor (istisna: `DropZone`'un sürükleme sırasındaki geçici state'i, o da QSS dynamic property seçicisiyle çözülüyor, renk kodu Python'da yok). Yeni bir widget stili eklerken: `main.qss`'e `objectName` seçicisi ekle, widget'a `setObjectName(...)` ver — bkz. [[RULES]]#kod-kuralları.

İlgili: [[core-servisleri]], [[teknoloji-yigini]], [[tema-sistemi]]
