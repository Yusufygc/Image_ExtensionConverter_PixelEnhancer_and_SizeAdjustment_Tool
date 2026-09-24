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

## Spinbox stepper okları

`FluentSpinBox` up/down stepper okları `Canvas` ile çiziliyor — `FluentComboBox`'ın hedef format chevron'uyla birebir aynı geometri (12×7, stroke 2.4, aynı path; up aynı path'in dikey aynası). Buton arka plan kutusu/border yok, sadece ok ikonu görünüyor. Stroke rengi `FluentTheme.accent` — tema değişince otomatik güncellenir (`Connections { target: FluentTheme; onIsDarkChanged }` ile `requestPaint()`).

## Sekme seçili dolgu rengi

`FluentTheme.tabActiveBg` token'ı — Dönüştür/Boyutlandır/Kalite Artır ana sekmelerinde (`ControlPanel.qml`) seçili durumun dolgu rengi. Detay: [[tema-sistemi]]#qml-tarafı-ui-qml-fluenttheme-qml.

## Toast konumu

`FluentToast` artık pencerenin üst-orta kısmında (`anchors.top` + `horizontalCenter`), yukarıdan aşağı kayarak beliriyor — eskiden sağ-alt köşedeydi. Bkz. `Main.qml`.

İlgili: [[core-servisleri]], [[teknoloji-yigini]], [[tema-sistemi]]
