# Conventor — Wiki İndeksi

Bu wiki, P006-Converter (Conventor / Uzantı Dönüştürücü ve Piksel Artırıcı) projesinin canlı bilgi tabanıdır. Kod yazmadan, mimari karar vermeden veya soru yanıtlamadan önce bu dosya okunur; gerekirse aşağıdaki linkler takip edilir. Çalışma kuralları için: [[RULES]]. Kronolojik değişiklik kaydı: [[log]].

## Mimari

- [[mimari]] — 3 katman (core/ui/utils), thread modeli, operasyon registry pattern, stil sistemi.
- [[core-servisleri]] — ConverterService/ResizerService/EnhancerService, interface sözleşmesi, hata yayılım kuralı.
- [[arayuz-katmani]] — MainWindow, widget'lar, ThemeManager, worker thread.
- [[merkezi-icon-ve-string-yapisi]] — AppIcons, UIStrings, get_icon() — tüm ikon/metin literal'lerinin merkezi kaynağı.
- [[tema-sistemi]] — token tabanlı dark/light tema, ThemeManager.toggle_theme(), QSettings kalıcılığı, header'daki toggle buton.

## Altyapı

- [[teknoloji-yigini]] — PySide6/Pillow/Nuitka/pytest, requirements dosya ayrımı, logging.
- [[build-ve-dagitim]] — build.bat (Nuitka), Inno Setup script'i, repo hijyeni (exe geçmişten temizlendi).
- [[test-stratejisi]] — pytest kapsamı, fixture'lar, hangi katman test edilmiyor ve neden.

## Kurallar

- [[RULES]] — commit mesajı formatı ve kod kuralları (bu projeye özel).

## Proje özeti

Conventor, PySide6 + Pillow tabanlı bir masaüstü uygulaması: resim formatı dönüştürme (JPEG/PNG/WEBP/BMP/ICO/TIFF/SVG), piksel/yüzde bazlı yeniden boyutlandırma, LANCZOS+UnsharpMask ile çözünürlük artırma. Nuitka ile tek dosya exe'ye derlenip Inno Setup ile paketleniyor.
