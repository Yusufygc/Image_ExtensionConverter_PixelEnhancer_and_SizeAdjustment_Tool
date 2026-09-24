# Build ve Dağıtım

## `build.bat`

PyInstaller ile `--onefile` derleme: `python -m PyInstaller --noconfirm --onefile --windowed --icon=assets/icons/icon.ico --name=Conventor --add-data "assets;assets" --add-data "ui/qml;ui/qml" --hidden-import=PIL --hidden-import=PySide6.QtQuick --hidden-import=PySide6.QtQml --hidden-import=PySide6.QtSvg main.py`. Çıktı: `dist/Conventor.exe`. PyInstaller kurulu değilse `requirements-build.txt`'ten kurulur (bkz. [[teknoloji-yigini]]).

`--windowed` ile konsol penceresi açılmaz; hata ayıklama dosyaya loglama ile yapılır (bkz. [[teknoloji-yigini]]#logging). Kaynak yolları `utils/path_helper.py` içindeki `sys._MEIPASS` çözümlemesi ile tek dosya açılım dizininden yüklenir.

## Kurulum sihirbazı (`Documents/deneme.iss`)

Inno Setup script'i. `.gitignore`'daki `/Documents/*` kuralına istisna tanımlanarak (`!/Documents/deneme.iss`) versiyonlanıyor — klasördeki diğer kişisel notlar (`plan.txt`, `sanalortamkurulum.txt`) repo dışı kalmaya devam ediyor. Script içindeki tüm yollar `{#SourcePath}` göreli referanslarıyla yazılı (eskiden geliştirici makinesine özel `D:\...`, `C:\ikonlar\...` mutlak yolları vardı, kaldırıldı) — başka bir makinede doğrudan çalıştırılabilir. Setup ikonu repodaki `assets/icons/icon.ico`'yu kullanıyor.

## Repo hijyeni: derlenmiş ikili dosyalar

`*.exe` ve `*.msi` `.gitignore`'da. Daha önce yanlışlıkla commit'lenmiş `ConverterApp.exe`, `git filter-repo` ile **tüm commit geçmişinden** temizlendi ve `origin/main`'e force-push edildi (rewrite öncesi tam repo yedeği alındı). Kural: derlenmiş ikili dosyalar asla commit'lenmez, dağıtım GitHub Releases üzerinden yapılır. Bkz. [[RULES]]#commit-kuralları.

## GitHub deposu

Repo `github.com/Yusufygc/Image_Conventor` adresinden `Image_ExtensionConverter_PixelEnhancer_and_SizeAdjustment_Tool` adına taşındı; eski URL redirect ile çalışmaya devam ediyor.

İlgili: [[teknoloji-yigini]], [[mimari]]
