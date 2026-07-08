# Build ve Dağıtım

## `build.bat`

Nuitka ile `--onefile` derleme: `python -m nuitka --onefile --enable-plugin=pyside6 --windows-console-mode=disable --windows-icon-from-ico=assets/icons/icon.ico --include-data-dir=assets=assets --main=main.py`. Çıktı: `dist/main.exe`. Nuitka/zstandard kurulu değilse `requirements-build.txt`'ten kurulur (bkz. [[teknoloji-yigini]]).

`--windows-console-mode=disable` önemli bir kısıt: paketlenmiş exe'nin konsolu yok, bu yüzden hata ayıklama `print()` ile değil dosyaya loglama ile yapılıyor (bkz. [[teknoloji-yigini]]#logging).

## Kurulum sihirbazı (`Documents/deneme.iss`)

Inno Setup script'i. `.gitignore`'daki `/Documents/*` kuralına istisna tanımlanarak (`!/Documents/deneme.iss`) versiyonlanıyor — klasördeki diğer kişisel notlar (`plan.txt`, `sanalortamkurulum.txt`) repo dışı kalmaya devam ediyor. Script içindeki tüm yollar `{#SourcePath}` göreli referanslarıyla yazılı (eskiden geliştirici makinesine özel `D:\...`, `C:\ikonlar\...` mutlak yolları vardı, kaldırıldı) — başka bir makinede doğrudan çalıştırılabilir. Setup ikonu repodaki `assets/icons/icon.ico`'yu kullanıyor.

## Repo hijyeni: derlenmiş ikili dosyalar

`*.exe` ve `*.msi` `.gitignore`'da. Daha önce yanlışlıkla commit'lenmiş `ConverterApp.exe`, `git filter-repo` ile **tüm commit geçmişinden** temizlendi ve `origin/main`'e force-push edildi (rewrite öncesi tam repo yedeği alındı). Kural: derlenmiş ikili dosyalar asla commit'lenmez, dağıtım GitHub Releases üzerinden yapılır. Bkz. [[RULES]]#commit-kuralları.

## GitHub deposu

Repo `github.com/Yusufygc/Image_Conventor` adresinden `Image_ExtensionConverter_PixelEnhancer_and_SizeAdjustment_Tool` adına taşındı; eski URL redirect ile çalışmaya devam ediyor.

İlgili: [[teknoloji-yigini]], [[mimari]]
