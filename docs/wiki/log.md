# Log

Kronolojik kayıt defteri. Yeni kayıtlar dosyanın **en üstüne** eklenir. Format: `## [YYYY-AA-GG] [İŞLEM_TİPİ] | Kısa Açıklama`. Navigasyon: [[index]].

## [2026-09-24] FEAT | Dark mod "Snack at Midnight" renk paleti uygulandı, header ikonu ve spinbox kutuları kaldırıldı, toast üst-orta konuma taşındı

- `ui/qml/FluentTheme.qml`: dark mod renkleri kullanıcının verdiği palet görseline göre değiştirildi — bgApp `#0F0807` (Crushed Cacao), bgCard `#432430` (Mulberry Night), textPrimary `#CEB3AB` (Champagne Silk), accent `#E8AC97` (Glace Apricot), tabActiveBg/seçili durum `#2A3548` (Indigo Tart). Light mod dokunulmadı.
- Palet ile çakışan component-lokal hardcoded gri renkler (`FluentButton`, `FluentIconButton`, `FluentScrollBar`, `FluentProgressBar`, `DropZoneArea`, `FileCardItem`, `FileListItem`, `FluentComboBox`) sıcak tona hizalandı.
- `ui/qml/Main.qml`: header'daki uygulama ikonu (başlık yanındaki icon) kaldırıldı — sadece metin kaldı.
- `ui/qml/components/FluentSpinBox.qml`: up/down stepper butonlarının arka plan kutusu/border'ı kaldırıldı, sadece ok ikonları kaldı; ok rengi `FluentTheme.accent` oldu (tema değişince otomatik güncelleniyor).
- `ui/qml/Main.qml` + `FluentToast.qml`: toast bildirimi sağ-alttan üst-orta konuma taşındı, giriş animasyonu yukarıdan aşağı kaymaya çevrildi.
- Önceki `down_arrow_v2.svg`/`up_arrow_v2.svg` aday dosyaları (kullanılmadı) silindi.

İlgili: [[tema-sistemi]], [[arayuz-katmani]]

## [2026-09-24] INGEST | Uygulama ikonu (icon.ico) için alternatif aday oluşturuldu

Kullanıcı önceki "iconu beğenmedim" mesajının ok ikonları değil `assets/icons/icon.ico` (uygulama/taskbar ikonu, `AppIcons.APP`) için olduğunu belirtti. Mevcut `icon.ico` (64x64, düz mavi, jenerik stok görünüm) yerine Fluent üslubuna uyan aday üretildi:
- `assets/icons/icon_v2.ico` — 16/24/32/48/64/128/256 boyutlu multi-size ico, gradient buz mavisi (`#2E9BE6`→`#0067C0`) zemin, fotoğraf çerçevesi + dönüştürme (refresh) rozeti glifi.
- Kullanıcı onayladı: `icon_v2.ico` 16/24/32/48/64/128/256 boyutlarıyla `assets/icons/icon.ico` üzerine yazıldı (aday dosya silindi). `AppIcons.APP` ve `build.bat --icon=assets/icons/icon.ico` zaten bu path'e işaret ettiği için ek kod değişikliği gerekmedi.

İlgili: [[merkezi-icon-ve-string-yapisi]], [[build-ve-dagitim]]

## [2026-09-24] FEAT | Spinbox stepper ikonları SVG'ye taşındı, aktif sekme dolgusu buz mavisi yapıldı

Kullanıcı isteği: hedef format combobox'ında kullanılan down/up ok görselinin boyutlandır ve kalite artır alanlarındaki spinbox stepper butonlarında da kullanılması, ayrıca Dönüştür/Boyutlandır/Kalite Artır sekmelerinin seçili dolgu renginin soluk buz mavisi olması.
- `ui/qml/components/FluentSpinBox.qml`: Up/Down stepper butonlarındaki Canvas ile çizilen chevron'lar kaldırıldı, yerine `bridge.icons.upArrow` / `bridge.icons.downArrow` (`assets/icons/up-arrow.svg`, `down-arrow.svg`) kullanan `Image` bileşenleri kondu.
- `ui/qml/FluentTheme.qml`: Yeni token `tabActiveBg` eklendi (dark: `#22384A`, light: `#E3F2FB` — soluk buz mavisi).
- `ui/qml/views/ControlPanel.qml`: 3 ana işlem sekmesinin (Tab 1/2/3) seçili durum dolgu rengi eski `#383838`/`#FFFFFF` yerine `FluentTheme.tabActiveBg` oldu.
- Not: Kullanıcı mevcut ok ikonunu (`#89b4fa` stroke, `down-arrow.svg`/`up-arrow.svg`) beğenmedi; alternatif adaylar `assets/icons/down_arrow_v2.svg` / `up_arrow_v2.svg` olarak kaydedildi (nötr `#1A1A1A`, ince 1.6px stroke), kod henüz bunlara bağlanmadı — kullanıcı onayı bekleniyor.

İlgili: [[arayuz-katmani]], [[tema-sistemi]], [[merkezi-icon-ve-string-yapisi]]

## [2026-09-24] FIX | FluentScrollBar 'contentItem' ve 'background' stil uyarıları çözüldü

Windows yerel stili altında özel ScrollBar özelleştirme uyarısı çözüldü:
- `main.py`: `QQuickStyle.setStyle("Basic")` ayarlanarak Qt Quick Controls'ün özelleştirilebilir temel stile geçmesi sağlandı.
- `ui/qml/components/FluentScrollBar.qml`: `import QtQuick.Controls` yerine doğrudan `import QtQuick.Controls.Basic` kullanılarak `contentItem` ve `background` özelleştirmelerinin tam destekle, sıfır konsol uyarısıyla çalışması sağlandı.

## [2026-09-24] FEAT | 'Dosya Ekle' butonu üst araç çubuğuna geri eklendi

Kullanıcı isteği doğrultusunda "Dosya Ekle" butonu üst araç çubuğuna yeniden entegre edildi:
- `ui/qml/views/FilesPanel.qml`: Sol üst araç çubuğuna `FluentButton` ile "Dosya Ekle" butonu (upload ikonu ile) eklendi. Buton tıklandığında `bridge.browseFiles()` tetikleniyor.
- `ui/qml/views/AboutModal.qml`: Kullanım kılavuzundaki dosya ekleme adımı güncellendi.

## [2026-09-24] FIX | Uygulama kapanışındaki QML 'Cannot read property of null' hataları çözüldü

Uygulama kapatılırken Python garbage collector'ın `bridge` nesnesini QML motorundan önce yok etmesi sonucu oluşan hata silsilesi giderildi:
- `main.py`: `bridge = AppBridge(app)` ile `AppBridge` nesnesi `app`'e bağlandı (C++ yaşam döngüsü güvenliği). `app.aboutToQuit` ile çalışan arka plan iş parçacıklarının güvenli durdurulması sağlandı. `del engine` ile QML motoru ve nesne ağacı `bridge` ve `app` henüz canlıyken kontrollü biçimde imha edildi.
- `ui/qml/Main.qml`: `onClosing` sinyali eklendi; `bridge` bağlamı için savunmacı kontroller (`bridge ? ... : ...`) sağlandı.

## [2026-09-24] FIX | Koyu modda siyah kalan ikonlar reaktif beyaz renge uyarlandı

Kullanıcı bildirimi doğrultusunda koyu modda görünmez olan/siyah kalan ikonlar düzeltildi:
- `ui/qml/components/FluentIconButton.qml`: `QtQuick.Effects` `MultiEffect` entegre edildi. `tintWithTheme` özelliği ile koyu temada (`isDark: true`) siyah/monokrom ikonların (Grid, Liste, Klasör Aç, Bilgi vb.) parlak beyaz (`#FFFFFF`) görünmesi, açık temada ise orijinal koyu tonunu koruması sağlandı.
- `ui/qml/components/FluentButton.qml`: Buton içi ikonlara `MultiEffect` desteği kazandırılarak "Tümünü Temizle" vb. butonlardaki SVG ikonların koyu modda aydınlatılması sağlandı.
- `ui/qml/Main.qml`: Tema değiştirme butonu (`sun`/`moon`) için `tintWithTheme: false` verilerek orijinal sarı ve mavi renkleri korundu.

## [2026-09-24] FEAT | 4 Resim sığacak pencere boyutu & Modern Fluent ScrollBar

Kullanıcı gereksinimi doğrultusunda pencere boyutlandırması ve kaydırma çubuğu yenilendi:
- `ui/qml/Main.qml`: Varsayılan pencere boyutu 1180x740 (minimum 1040x640) olarak ayarlandı. Sağ panel ideal genişlikte (~380-400px) tutularak sol panelin her zaman en az 4 görsel sütununu rahatça sığdırması sağlandı.
- `ui/qml/components/FluentScrollBar.qml`: Eski ilkel ve siyah kutulu Basic style ScrollBar yerine; Windows 11 Fluent tasarımına uygun, belirgin iz (track) çizgisine ve yüksek kontrastlı yuvarlatılmış tutamağa (pill thumb) sahip modern kaydırma çubuğu bileşeni oluşturuldu.
- `ui/qml/views/FilesPanel.qml`: `ScrollView` sarmalayıcısı yerine doğrudan `GridView` ve `ListView` üzerine `FluentScrollBar` bağlandı. Sütun genişliği `width - 14px` üzerinden dinamik hesaplanarak kaydırma çubuğu açıldığında bile 4 sütunun bozulmadan korunması garanti altına alındı.

## [2026-09-24] REFACTOR | Açılır liste (ComboBox) aşağı oku kalınlaştırıldı

- `ui/qml/components/FluentComboBox.qml`: Silik ve ince kalan `Image` oku kaldırılarak, stepper oklarıyla tam uyumlu, 2.2px kalınlığında, yuvarlatılmış uçlu, koyu ve yüksek kontrastlı (`#2B2D31` / dark modda `#E0E0E0`, hover durumunda siyah/beyaz, açıkken accent rengi) dinamik vektör `Canvas` chevron eklendi.

## [2026-09-24] REFACTOR | Üst araç çubuğundaki 'Dosya Ekle' butonu kaldırıldı

Kullanıcı geri bildirimi doğrultusunda sol panel üst araç çubuğundaki "Dosya Ekle" butonu kaldırıldı:
- `ui/qml/views/FilesPanel.qml`: Araç çubuğu sadeleştirildi; görünüm değiştirici (Grid/Liste) ve sıralama menüsü bırakıldı.
- Dosya ekleme işlemi doğrudan orta alandaki interaktif `DropZoneArea` (tıklama ve sürükle-bırak) ve liste üzerindeki `DropArea` ile yürütülüyor.
- `ui/qml/views/AboutModal.qml`: Kullanım kılavuzu açıklaması güncellendi.

## [2026-09-24] CHORE | Nuitka kaldırıldı, paketleme PyInstaller'a taşındı

Kullanıcı isteği doğrultusunda build aracı Nuitka'dan PyInstaller'a geçirildi:
- `requirements-build.txt`: `nuitka` ve `zstandard` kaldırıldı, `pyinstaller==6.22.3` eklendi.
- `build.bat`: PyInstaller `--onefile --windowed --name=Conventor` komutuyla güncellendi (`assets` ve `ui/qml` dizinleri dahil edildi).
- `utils/path_helper.py`: Mevcut `sys._MEIPASS` PyInstaller desteği aktif olarak kullanılmaya devam ediyor.
- Dokümantasyon (`README.md`, `docs/wiki/build-ve-dagitim.md`, `docs/wiki/teknoloji-yigini.md`, `docs/wiki/index.md`) güncellendi.

## [2026-09-24] FEAT | PySide6 QML Windows 11 Fluent Split-View Arayüzü Eklendi

Kullanıcı gereksinimleri doğrultusunda `core/` (backend) katmanına kesinlikle dokunulmadan `ui/` katmanı modernize edildi:
- `ui/bridge.py` (`AppBridge`): MVVM köprüsü olarak QML ile mevcut `core/` servisleri ve `ui/worker.py` arasında reaktif bağlantı kurar.
- Windows 11 Fluent Split-View: Sol panelde dosyalar/thumbnail'lar (Grid ve Liste modları, çoklu seçim, ada/boyuta/duruma göre sıralama, sürükle-bırak dropzone), sağ panelde işlem parametreleri, hedef klasör seçimi + "Klasörü Aç" butonu ve aksiyon paneli.
- Sıfır emoji kuralı: Tüm durumlar için temiz SVG/vektör ikonlar (`check_icon.svg`, `error_icon.svg`, `sort_icon.svg`, `grid_icon.svg`, `list_icon.svg`, `open_folder_icon.svg`, `trash_icon.svg`, vector canvas spinner).
- Nuitka build yapılandırması: `build.bat` içine `--include-data-dir=ui/qml=ui/qml` eklendi.
- Birim testleri: `tests/test_bridge.py` (6 yeni test) eklendi, tüm 20 pytest testi başarıyla geçti. Detay: [[arayuz-katmani]], [[mimari]].

## [2026-09-24] REVIEW | Toast/tema commit'lerinin denetimi, 8 bulgu çözüldü + önizleme büyütüldü

`AI-Gelistirme-Metodolojisi.md`ye göre yapılan code review'da, wiki'ye hiç işlenmemiş 2 commit'te (toast bildirimi, arayüz hizalamaları) 8 bulgu tespit edilip çözüldü: `utils/svg_colorizer.py`'de her `apply_theme()` çağrısında sızan/tekrar üretilen temp SVG dosyaları için `(path, color_hex)` cache'i eklendi (kritik); `main_window.py`, `drop_zone.py`, `toast.py`'deki literal string ve inline `setStyleSheet()` ihlalleri `UIStrings`/`main.qss`'e taşındı; kullanılmayan `set_app_instance()` silindi; `file_list_item.py`'deki duplicate import'lar ve sessizce yutulan `except Exception` blokları (artık `logging.warning`) düzeltildi. Ayrıca kullanıcı isteğiyle dosya listesi önizleme thumbnail'ı büyütüldü (48px -> 96px, `AppConstants.FILE_ITEM_THUMB_SIZE` vb. sabitlere taşındı). `pytest` (14/14) her adımdan sonra doğrulandı. Detay: [[arayuz-katmani]].

## [2026-07-08] FEAT | Token tabanlı dark/light tema sistemi + toggle buton

`ui/styles/tokens.py`'ye `DARK_TOKENS` (Catppuccin Mocha) / `LIGHT_TOKENS` (Catppuccin Latte) eklendi; `assets/style/main.qss`'teki tüm literal renkler `@color_*` placeholder'larına çevrildi. `ThemeManager`'a saf `render_qss()`, `apply_theme(theme=None)`, `toggle_theme()` eklendi; tema tercihi `QSettings` ile kalıcı, ilk açılış varsayılanı `light`. Header'daki dengeleme amaçlı boş `dummy_btn` yerine gerçek `btn_theme_toggle` (sol üst, sun/moon ikonlu) geldi. `tests/test_theme.py` ile token anahtar eşitliği ve placeholder temizliği garanti altına alındı. QML'e geçiş ayrıca tartışıldı, kapsam dışı bırakıldı (mevcut ölçek için gerekçe yetersiz). Detay: [[tema-sistemi]].

## [2026-07-08] INGEST | LLM Wiki mekanizması kuruldu

`docs/wiki/` bilgi tabanı ve `CLAUDE.md` "anayasa" dosyası oluşturuldu. Sayfalar: [[mimari]], [[core-servisleri]], [[arayuz-katmani]], [[merkezi-icon-ve-string-yapisi]], [[teknoloji-yigini]], [[build-ve-dagitim]], [[test-stratejisi]], [[RULES]]. Bundan sonra INGEST/QUERY/LINT komutları geçerli — detay `CLAUDE.md`'de.

## [2026-07-08] REFACTOR | Merkezi icon ve string yapısı kuruldu

`utils/constants.py`'ye `AppIcons`, yeni `utils/strings.py`'ye `UIStrings` eklendi; `utils/path_helper.py`'ye `get_icon()` yardımcı fonksiyonu eklendi (5 yerde tekrarlanan exists+QIcon deseni sadeleşti). 6 UI dosyası (`main_window.py`, `theme.py`, `drop_zone.py`, `file_list_item.py`, `info_view.py`, `worker.py`) hardcoded path/string yerine bu sabitleri kullanacak şekilde güncellendi. Detay: [[merkezi-icon-ve-string-yapisi]].

## [2026-07-08] FIX | 18 denetim bulgusu çözüldü, git geçmişi temizlendi

`V2-GenelSablon.md` şablonuna göre yapılan denetimde bulunan 18 bulgu (3 Kritik, 6 Yüksek, 8 Orta, 1 Düşük — orijinal 20'den 2'si diğerleriyle birleşti) çözüldü: toplu işlemde kısmi hata bildirimi, worker güvenli kapanışı, `core/` için pytest paketi, interface imza uyumu, logging altyapısı, bağımlılık pinleme, stil merkezileştirme (`QLabel#DropZone` → `QFrame#DropZone` seçici hatası dahil), `main_window.py`'nin builder metotlarına bölünmesi ve operasyon registry pattern'i. Ayrıca `ConverterApp.exe` `git filter-repo` ile tüm commit geçmişinden temizlenip `origin/main`'e force-push edildi (önce `git bundle` ile tam yedek alındı). Detay: [[mimari]], [[core-servisleri]], [[arayuz-katmani]], [[build-ve-dagitim]], [[test-stratejisi]].
