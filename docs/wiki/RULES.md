# Kurallar

Bu proje için commit ve kod kuralları. Wiki bağlamı: [[index]].

## Commit Kuralları

- Format: `<tip>: <kısa açıklama (Türkçe, emir kipi değil, "ne yapıldı")>`. Tipler: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`.
- Konu satırı ~70 karakteri geçmez; gövde gerekiyorsa (neden/etki açıklaması) boş satırdan sonra yazılır.
- Bir commit tek bir mantıksal değişikliği taşır. Aynı dosyada birbirinden bağımsız birden fazla değişiklik varsa (örn. bir refactor + ayrı bir bugfix aynı dosyada), mümkünse ayrı commit'lere bölünür; dosya bütünlüğü bozuluyorsa (interaktif `git add -p` gerektirecek kadar iç içeyse) tek commit'te toplanıp mesajda madde madde açıklanır.
- Derlenmiş ikili dosya (`.exe`, `.msi`, `dist/`, `build/`) **asla** commit'lenmez — bkz. [[build-ve-dagitim]]#repo-hijyeni-derlenmiş-ikili-dosyalar.
- Yıkıcı git işlemleri (`push --force`, `filter-repo`, `reset --hard`) önce kullanıcıdan açık onay alınmadan yapılmaz; onay alınsa bile önce yedek (`git bundle`) alınır.
- Sadece kullanıcı açıkça istediğinde commit atılır — kod değişikliği yapıldı diye otomatik commit atılmaz.
- ai referansı verme 

## Kod Kuralları

- **Katman sınırı:** `core/` hiçbir zaman `PySide6` import etmez (bkz. [[mimari]]). Qt'ye ihtiyaç varsa o kod `ui/` veya `utils/`'a aittir.
- **Literal yasak:** Yeni ikon dosyası veya arayüz metni eklerken doğrudan string yazılmaz — önce `utils/constants.py`'deki `AppIcons` veya `utils/strings.py`'deki `UIStrings`'e sabit eklenir, sonra kullanılır. Bkz. [[merkezi-icon-ve-string-yapisi]].
- **Stil:** Widget'a inline `setStyleSheet()` yazılmaz. `main.qss`'e `objectName` seçicili kural eklenir, widget'a `setObjectName(...)` verilir. İstisna: gerçekten dinamik/runtime state (örn. sürükleme sırasında renk değişimi) — o da Qt dynamic property + `style().polish()` deseniyle çözülür, ham renk kodu Python'da yazılmaz.
- **Hata yönetimi:** `print()` kullanılmaz (paketlenmiş exe'de konsol kapalı — bkz. [[teknoloji-yigini]]#logging), `logging.exception()` / `logging.warning()` kullanılır. Beklenen hata tipleri (örn. `FileNotFoundError`) generic `Exception`'a sarılıp yutulmaz.
- **DRY:** Aynı `os.path.exists()` + kaynak yükleme deseni 2'den fazla yerde tekrarlanıyorsa ortak bir yardımcıya çıkarılır (örnek: `get_icon()`, `load_image()`).
- **Test:** `core/` katmanına yeni davranış eklenirken (yeni format, yeni parametre, yeni hata yolu) `tests/`'e karşılık gelen bir test eklenir. Bkz. [[test-stratejisi]].
- **Bağımlılıklar:** Runtime (`requirements.txt`), build-time (`requirements-build.txt`) ve dev-time (`requirements-dev.txt`) bağımlılıkları ayrı dosyalarda tutulur, sürümler pinlenir (`==`). Bkz. [[teknoloji-yigini]].
- **Yorum satırları:** Sadece "neden" nonobvious olduğunda yazılır (gizli kısıt, workaround, sürpriz davranış). "Ne yapıyor" açıklaması yazılmaz — isimlendirme bunu zaten anlatmalı.
