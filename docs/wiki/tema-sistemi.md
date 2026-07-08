# Tema Sistemi (Dark/Light Toggle)

Üst bağlam: [[arayuz-katmani]], [[merkezi-icon-ve-string-yapisi]] (aynı "literal yasak, merkezi sabit" felsefesinin renklere uygulanmış hali).

## Token mimarisi

`ui/styles/tokens.py` iki dict tanımlıyor: `DARK_TOKENS` (Catppuccin Mocha — orijinal palet, birebir korunuyor) ve `LIGHT_TOKENS` (Catppuccin Latte — Mocha'nın resmi eşi). ~37 semantik anahtar (`bg_window_start`, `text_primary`, `accent`, `danger_bg`, `dropzone_hover_bg` vb.) — her ikisi de aynı anahtar kümesini paylaşmak zorunda, `tests/test_theme.py::test_dark_and_light_tokens_have_identical_keys` bunu garanti ediyor.

`assets/style/main.qss`'teki tüm literal hex/rgba renk kodları `@color_<token>` placeholder'larına çevrildi (mevcut `@icon_down_arrow` ikon-placeholder desenine paralel).

## `ui/styles/theme.py`

- `render_qss(qss_template, color_tokens, icon_paths) -> str` — saf fonksiyon, `@icon_*` ve `@color_*` placeholder'larını değiştirir. Qt'ye bağımlı değil, `tests/test_theme.py`'de doğrudan test ediliyor.
- `ThemeManager.apply_theme(app, theme=None)` — `theme` verilmezse `QSettings`'ten okunur (yoksa `"light"` varsayılan — ilk açılışta light gelir). QSS'i render edip `app.setStyleSheet()` ile uygular, seçimi `QSettings`'e yazar.
- `ThemeManager.toggle_theme(app) -> str` — `light`↔`dark` çevirir.
- Kalıcılık: `QSettings("MYY Yazılım", AppConstants.APP_NAME)`, anahtar `"theme"` (Windows'ta registry: `HKEY_CURRENT_USER\Software\MYY Yazılım\...`).

## Toggle buton

`ui/main_window.py` header'ında, eskiden sadece görsel denge için duran boş `dummy_btn`'in yerine `self.btn_theme_toggle` (sol üst, `IconOnlyButton`) geldi. İkon, tıklanınca geçilecek temayı gösteriyor (dark aktifken ☀️, light aktifken 🌙 — `toggle_info_page()`'deki ikon-değiştirme deseniyle aynı mantık). `MainWindow.__init__` içinde `ThemeManager.apply_theme()` artık `setup_ui()`'dan ÖNCE çağrılıyor ki header kurulurken `ThemeManager.current_theme` zaten doğru olsun (yanlış ikonla açılıp düzelme "flash"ı olmasın).

Yeni ikonlar: `assets/icons/sun.svg`, `moon.svg` — `AppIcons.THEME_SUN`/`THEME_MOON`, fallback metinleri `UIStrings.FALLBACK_THEME_SUN`/`FALLBACK_THEME_MOON`.

## Bilinen sınır

Mevcut ikonların çoğu (`info_icon.svg`, `delete_icon.svg` vb.) stroke rengi SVG içine sabit hardcoded — temaya göre otomatik renk değiştirmiyor. Bu, SVG recolor (runtime'da `QPainter` ile yeniden boyama) gerektirir; kapsam dışı bırakıldı, mevcut renkler her iki temada da okunabilir kabul edildi.

## Yeni token eklerken

`main.qss`'e yeni bir renk gerektiğinde: önce `tokens.py`'deki her iki dict'e de aynı anahtarı ekle, sonra QSS'te `@color_<anahtar>` kullan. Sadece `DARK_TOKENS`'e eklenip `LIGHT_TOKENS`'i unutursan test kırılır (kasıtlı guard). Bkz. [[RULES]]#kod-kuralları.
