# Arayüz Katmanı

`ui/` PySide6 üzerine kurulu. Üst bağlam: [[mimari]].

## Dosyalar ve Bileşenler

- **`bridge.py`** — `AppBridge` (QObject). QML ile backend ve worker arasındaki MVVM köprüsü. Dosya listesi, operasyon ayarları, sıralama, çoklu seçim ve tema durumunu `Q_PROPERTY` ve sinyallerle yönetir.
- **`qml/`** — Windows 11 Fluent Split-View arayüzü:
  - `Main.qml`: Ana pencere kabuğu (`ApplicationWindow`).
  - `FluentTheme.qml`: Windows 11 Fluent renk token'ları (Dark & Light) ve tipografi.
  - `views/FilesPanel.qml`: Sol panel (DropZone, Grid/Liste görünümleri, sıralama, toplu silme, çoklu seçim).
  - `views/ControlPanel.qml`: Sağ panel (İşlem sekmeleri, dinamik parametreler, hedef klasör + tek tıkla klasörü açma, progress bar ve başlat butonu).
  - `views/AboutModal.qml`: Bilgi ve yardım modalı.
  - `components/`: `FluentCard`, `FluentButton`, `FluentIconButton`, `FluentComboBox`, `FluentSpinBox`, `FluentProgressBar`, `FluentToast`, `LoadingSpinner`, `DropZoneArea`, `FileCardItem`, `FileListItem`.
- **`worker.py`** — `ProcessingWorker` (QThread) + `WorkerSignals`. Bkz. [[mimari]]#thread-modeli.
- **`main_window.py`** — Eski QtWidgets tabanlı `MainWindow` (geriye dönük referans olarak muhafaza edildi).
- **`styles/theme.py`** — `ThemeManager`, token tabanlı dark/light tema motoru. Detay: [[tema-sistemi]].

## Merkezi ikon/string yapısı

Hiçbir dosyada `"assets/icons/..."` gibi literal path veya hardcoded Türkçe metin yok — hepsi `AppIcons` / `UIStrings` üzerinden. Detay: [[merkezi-icon-ve-string-yapisi]].

## Stil kuralı

Inline `setStyleSheet()` kullanılmıyor (istisna: `DropZone`'un sürükleme sırasındaki geçici state'i, o da QSS dynamic property seçicisiyle çözülüyor, renk kodu Python'da yok). Yeni bir widget stili eklerken: `main.qss`'e `objectName` seçicisi ekle, widget'a `setObjectName(...)` ver — bkz. [[RULES]]#kod-kuralları.

## Tema ikonları — SVG renklendirme

`utils/svg_colorizer.py` (`get_tinted_icon`, `create_tinted_svg_file`) SVG içindeki `stroke`/`fill` renklerini regex ile tema rengine boyuyor; `ThemeManager.get_themed_icon()` ve `render_qss()`'in `@icon_*` placeholder'ları buradan besleniyor. `create_tinted_svg_file` her çağrıda yeni temp dosya yazmak yerine `(path, color_hex)` anahtarlı bir modül-seviyesi cache kullanıyor — aksi halde her `apply_theme()`/`toggle_theme()` çağrısında (ör. tema butonuna her tıklamada) diskte kalıcı temp dosya birikirdi. Cache `atexit` ile kapanışta temizleniyor. Detay: [[teknoloji-yigini]].

## Spinbox stepper ikonları

`FluentSpinBox` up/down stepper butonları artık Canvas çizimi yerine `bridge.icons.upArrow` / `bridge.icons.downArrow` (`assets/icons/up-arrow.svg`, `down-arrow.svg`) kullanıyor — hedef format `FluentComboBox`'ındaki chevron ile aynı görsel dil, boyutlandır ve kalite artır sekmelerindeki spinbox'larda da geçerli. Alternatif ikon adayları (`down_arrow_v2.svg`, `up_arrow_v2.svg`) kullanıcı onayı bekliyor, henüz koda bağlı değil.

## Sekme seçili dolgu rengi

`FluentTheme.tabActiveBg` token'ı (dark: `#22384A`, light: `#E3F2FB`) — Dönüştür/Boyutlandır/Kalite Artır ana sekmelerinde (`ControlPanel.qml`) seçili durumun dolgu rengi. Detay: [[tema-sistemi]].

İlgili: [[core-servisleri]], [[teknoloji-yigini]], [[tema-sistemi]]
