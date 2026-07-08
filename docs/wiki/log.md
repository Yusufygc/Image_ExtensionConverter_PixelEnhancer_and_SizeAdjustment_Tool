# Log

Kronolojik kayıt defteri. Yeni kayıtlar dosyanın **en üstüne** eklenir. Format: `## [YYYY-AA-GG] [İŞLEM_TİPİ] | Kısa Açıklama`. Navigasyon: [[index]].

## [2026-07-08] INGEST | LLM Wiki mekanizması kuruldu

`docs/wiki/` bilgi tabanı ve `CLAUDE.md` "anayasa" dosyası oluşturuldu. Sayfalar: [[mimari]], [[core-servisleri]], [[arayuz-katmani]], [[merkezi-icon-ve-string-yapisi]], [[teknoloji-yigini]], [[build-ve-dagitim]], [[test-stratejisi]], [[RULES]]. Bundan sonra INGEST/QUERY/LINT komutları geçerli — detay `CLAUDE.md`'de.

## [2026-07-08] REFACTOR | Merkezi icon ve string yapısı kuruldu

`utils/constants.py`'ye `AppIcons`, yeni `utils/strings.py`'ye `UIStrings` eklendi; `utils/path_helper.py`'ye `get_icon()` yardımcı fonksiyonu eklendi (5 yerde tekrarlanan exists+QIcon deseni sadeleşti). 6 UI dosyası (`main_window.py`, `theme.py`, `drop_zone.py`, `file_list_item.py`, `info_view.py`, `worker.py`) hardcoded path/string yerine bu sabitleri kullanacak şekilde güncellendi. Detay: [[merkezi-icon-ve-string-yapisi]].

## [2026-07-08] FIX | 18 denetim bulgusu çözüldü, git geçmişi temizlendi

`V2-GenelSablon.md` şablonuna göre yapılan denetimde bulunan 18 bulgu (3 Kritik, 6 Yüksek, 8 Orta, 1 Düşük — orijinal 20'den 2'si diğerleriyle birleşti) çözüldü: toplu işlemde kısmi hata bildirimi, worker güvenli kapanışı, `core/` için pytest paketi, interface imza uyumu, logging altyapısı, bağımlılık pinleme, stil merkezileştirme (`QLabel#DropZone` → `QFrame#DropZone` seçici hatası dahil), `main_window.py`'nin builder metotlarına bölünmesi ve operasyon registry pattern'i. Ayrıca `ConverterApp.exe` `git filter-repo` ile tüm commit geçmişinden temizlenip `origin/main`'e force-push edildi (önce `git bundle` ile tam yedek alındı). Detay: [[mimari]], [[core-servisleri]], [[arayuz-katmani]], [[build-ve-dagitim]], [[test-stratejisi]].
