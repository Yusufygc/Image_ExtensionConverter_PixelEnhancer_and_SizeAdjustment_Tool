# Merkezi Icon ve String Yapısı

Üst bağlam: [[arayuz-katmani]]. Kapsam: çoklu dil (i18n) altyapısı DEĞİL — sadece tek dilde (Türkçe) dağınık literal'leri iki modülde toplama.

## `utils/constants.py` → `AppIcons`

Her ikon dosyası (`assets/icons/*.svg`, `icon.ico`) ve `assets/style/main.qss` için birer path sabiti. Örn. `AppIcons.INFO = "assets/icons/info_icon.svg"`. `AppConstants` ile aynı dosyada, ayrı sınıf.

## `utils/strings.py` → `UIStrings`

Tüm Türkçe arayüz metni: buton/label metinleri, `QMessageBox` başlık/gövdeleri, `QFileDialog` başlık+filtre, durum çubuğu şablonları, `DropZone` durum metinleri, ikon bulunamazsa gösterilecek fallback glyph'ler (`"?"`, `"X"`, `"📂"` vb.), `ProcessingWorker` ilerleme/hata şablonları, `InfoView`'ın büyük HTML içerik bloğu. Şablon string'ler `.format()` ile dolduruluyor (örn. `UIStrings.STATUS_PARTIAL_ERROR_TEMPLATE.format(count=...)`).

## `utils/path_helper.py` → `get_icon()`

Önceden 5 ayrı yerde tekrarlanan desen:
```python
path = get_resource_path("assets/icons/x.svg")
if os.path.exists(path):
    widget.setIcon(QIcon(path))
else:
    widget.setText("fallback")
```
tek fonksiyona indirildi:
```python
icon = get_icon(AppIcons.X)
if icon:
    widget.setIcon(icon)
else:
    widget.setText(UIStrings.FALLBACK_X)
```
`get_icon()` dosya yoksa `None` döner ve `logger.warning(...)` ile loglar (bkz. [[teknoloji-yigini]]#logging); fallback metnini seçmek çağırana kalıyor çünkü her widget için farklı.

**Not:** `QPixmap` kullanan yerler (`DropZone`'un büyük önizleme ikonu, `FileListItemWidget`'ın thumbnail fallback'i) `get_icon()`'u kullanmıyor — sadece path'i `AppIcons`'tan alıp `QPixmap` ile kendi ölçekleme mantığını çalıştırıyor, çünkü `get_icon()` `QIcon` döndürüyor.

## Kural

Yeni bir ikon veya arayüz metni eklerken literal string yazmak yasak — önce `AppIcons`/`UIStrings`'e sabit ekle, sonra kullan. Bkz. [[RULES]]#kod-kuralları.
