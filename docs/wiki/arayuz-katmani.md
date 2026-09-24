# Arayüz Katmanı

`ui/` PySide6 üzerine kurulu. Üst bağlam: [[mimari]].

## Dosyalar

- **`main_window.py`** — `MainWindow`. `setup_ui()` iki sayfalı bir `QStackedWidget` kurar (Ana sayfa / Bilgi sayfası). Ana sayfa kurulumu builder metotlarına bölünmüş: `_build_file_selection_group()`, `_build_operation_group()`, `_build_option_widgets()`, `_build_output_folder_selector()`, `_build_progress_section()`. Operasyon seçimi registry pattern kullanıyor (bkz. [[mimari]]#operasyon-seçimi-registry-pattern).
- **`worker.py`** — `ProcessingWorker` (QThread) + `WorkerSignals`. Bkz. [[mimari]]#thread-modeli.
- **`styles/theme.py`** — `ThemeManager`, token tabanlı dark/light tema motoru. Detay: [[tema-sistemi]].
- **`views/info_view.py`** — statik bilgi sayfası, tüm metni `UIStrings.INFO_HTML_CONTENT`'ten alıyor.
- **`widgets/drop_zone.py`** — `DropZone` (QFrame). Sürükle-bırak sırasında `AppConstants.SUPPORTED_EXTENSIONS` ile dosya uzantısı filtreleniyor; desteklenmeyen dosya bırakılırsa kısa süreli uyarı metni gösterip (`QTimer.singleShot`) varsayılan metne dönüyor.
- **`widgets/file_list_item.py`** — `FileListItemWidget`. Küçük resim önizlemesi `QImageReader.setScaledSize()` ile hedef boyutta decode ediliyor (tam çözünürlükte yükleyip küçültmek yerine — büyük dosyalarda gereksiz bellek/CPU kullanımını önlüyor). Önizleme boyutu `AppConstants.FILE_ITEM_THUMB_SIZE` (96px) / `FILE_ITEM_THUMB_FALLBACK_ICON_SIZE` (64px) / `FILE_ITEM_ROW_HEIGHT` (116px) sabitlerinden geliyor; liste satır yüksekliği (`main_window.py`'de `item.setSizeHint`) bu sabitle senkron tutulmalı.
- **`widgets/toast.py`** — `ToastNotification` (frameless, `WA_TranslucentBackground` + `WindowStaysOnTopHint` geçici QWidget). `QGraphicsOpacityEffect` ile fade-in/fade-out, `QTimer.singleShot` ile otomatik kapanış. Stili `QLabel#ToastLabel` seçicisiyle `main.qss`'te — inline `setStyleSheet()` yok.

## Merkezi ikon/string yapısı

Hiçbir dosyada `"assets/icons/..."` gibi literal path veya hardcoded Türkçe metin yok — hepsi `AppIcons` / `UIStrings` üzerinden. Detay: [[merkezi-icon-ve-string-yapisi]].

## Stil kuralı

Inline `setStyleSheet()` kullanılmıyor (istisna: `DropZone`'un sürükleme sırasındaki geçici state'i, o da QSS dynamic property seçicisiyle çözülüyor, renk kodu Python'da yok). Yeni bir widget stili eklerken: `main.qss`'e `objectName` seçicisi ekle, widget'a `setObjectName(...)` ver — bkz. [[RULES]]#kod-kuralları.

## Tema ikonları — SVG renklendirme

`utils/svg_colorizer.py` (`get_tinted_icon`, `create_tinted_svg_file`) SVG içindeki `stroke`/`fill` renklerini regex ile tema rengine boyuyor; `ThemeManager.get_themed_icon()` ve `render_qss()`'in `@icon_*` placeholder'ları buradan besleniyor. `create_tinted_svg_file` her çağrıda yeni temp dosya yazmak yerine `(path, color_hex)` anahtarlı bir modül-seviyesi cache kullanıyor — aksi halde her `apply_theme()`/`toggle_theme()` çağrısında (ör. tema butonuna her tıklamada) diskte kalıcı temp dosya birikirdi. Cache `atexit` ile kapanışta temizleniyor. Detay: [[teknoloji-yigini]].

İlgili: [[core-servisleri]], [[teknoloji-yigini]], [[tema-sistemi]]
