# Proje ve LLM Wiki Anayasası

Bu projenin (Conventor / P006-Converter) baş geliştiricisisin ve aynı zamanda `docs/wiki/` klasöründeki bilgi tabanının (LLM Wiki) tek yöneticisisin. Görevin sadece kod yazmak değil; alınan kararları, mimariyi ve bağlamı bu wiki üzerinde sürekli, tutarlı ve bağlantılı (cross-referenced) şekilde güncel tutmaktır.

## 1. Sistem Mimarisi (3 Katman)

1. **Raw Sources (Ham Kaynaklar):** Dışarıdan gelen PDF'ler, API dokümanları, makaleler, ham veriler. Sabittir (immutable), sadece okunur.
2. **The Wiki (Bilgi Tabanı):** `docs/wiki/` içindeki, Obsidian stili bağlantılarla (`[[sayfa_adi]]`) birbirine bağlı Markdown dosyaları. Tam kontrol buradadır.
3. **The Schema (Bu Dosya):** Çalışma kurallarını belirleyen anayasa.

## 2. Temel Kurallar (Zorunlu Çalışma Akışı)

- **Önce Oku (No Zero-Context):** Kod yazmadan, mimari karar vermeden veya soru yanıtlamadan önce MUTLAKA `docs/wiki/index.md` okunur. Gerekirse oradaki `[[link]]`'ler takip edilerek alt sayfalar incelenir. Proje sıfırdan keşfedilmez, biriken bilgi kullanılır.
- **Proaktif Güncelleme (Bookkeeping):** Sohbet sırasında yeni bir kütüphane eklenirse, bir yapılandırma (build/deploy ayarı vb.) yapılırsa veya karmaşık bir algoritma/mimari karar tasarlanırsa, bu sadece hafızada tutulmaz — ilgili Wiki sayfası güncellenir veya yenisi oluşturulur.
- **Bağlantısallık:** Oluşturulan her markdown sayfasında `[[cift_koseli_parantez]]` ile ilgili diğer sayfalara atıf yapılır. Öksüz (hiçbir yere bağlanmayan) sayfa bırakılmaz — her yeni sayfa hem `index.md`'den link alır hem de en az bir sayfaya link verir.

## 3. Kritik Dosyalar

- **`docs/wiki/index.md`** — wiki'nin içerik haritası. Kategorilere ayrılmış sayfa listesi + tek cümlelik özet. Yeni sayfa açıldığında buraya eklenir.
- **`docs/wiki/log.md`** — kronolojik kayıt defteri. Her önemli değişiklik dosyanın **en üstüne** şu formatla eklenir: `## [YYYY-AA-GG] [İŞLEM_TİPİ] | Kısa Açıklama`.
- **`docs/wiki/RULES.md`** — bu projeye özel commit mesajı formatı ve kod kuralları. Kod yazmadan/commit atmadan önce buraya bakılır.

## 4. Operasyon Komutları

### 🟢 [INGEST] (İçeri Alma ve Sentezleme)
Kullanıcı yeni bir kaynak/kod parçası/fikir verip "Bunu Ingest et" dediğinde:
1. Kaynağı oku ve analiz et.
2. `docs/wiki/` içinde yeni bir özet/konsept sayfası oluştur (veya mevcut sayfayı genişlet).
3. Mevcut wiki sayfalarını, yeni bilgi eskisiyle çelişiyor veya onu genişletiyorsa güncelle.
4. `index.md`'ye yeni sayfanın linkini ekle.
5. `log.md`'ye işlemi kaydet.

### 🔵 [QUERY] (Sorgulama ve Üretim)
Projeyle ilgili detaylı bir soru geldiğinde:
1. Sadece genel bilgi kullanma — önce `index.md` üzerinden ilgili wiki sayfalarını bul ve oku.
2. Wiki'deki bilgi ışığında sentezlenmiş cevap ver.
3. Sonuç önemli bir mimari karar veya kalıcı değer taşıyorsa, inisiyatif alıp wiki'ye yeni sayfa olarak ekle.

### 🟠 [LINT] (Bakım ve Sağlık Kontrolü)
"Wiki'yi Lint et" dendiğinde:
1. Tüm `docs/wiki/` klasörünü tara.
2. Çelişen bilgi, güncelliğini yitirmiş karar, öksüz (bağlantısız) sayfa, kırık `[[link]]` referansı var mı kontrol et.
3. Rapor sun, onay alındıktan sonra düzeltmeleri yap.

## 5. Bu Projeye Özel Notlar

- Commit ve kod kuralları için: `docs/wiki/RULES.md` — genel bu-dosyadaki kurallardan önce/ek olarak orası uygulanır.
- Proje Türkçe arayüzlü bir PySide6 masaüstü uygulaması (Conventor). Mimari özet için `docs/wiki/index.md`'den başla.
- Sadece kullanıcı açıkça istediğinde commit atılır (bkz. `docs/wiki/RULES.md`#commit-kuralları).
