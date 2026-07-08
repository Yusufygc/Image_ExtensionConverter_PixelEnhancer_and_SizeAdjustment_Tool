from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from PySide6.QtCore import Qt
from utils.constants import AppConstants

class InfoView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10) # Reduced spacing
        layout.setContentsMargins(20, 20, 20, 20) # Reduced margins

        # Version (Title removed as it is in header)
        version = QLabel(f"Versiyon: {AppConstants.VERSION}")
        version.setObjectName("VersionLabel")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        # Content (Instructions)
        content = QLabel()
        content.setObjectName("InfoContentLabel")
        content.setWordWrap(True)
        content.setOpenExternalLinks(True)
        
        html_content = """
        <h3 style="color: #fab387; margin-bottom: 10px;">Nasıl Kullanılır?</h3>
        <div style="line-height: 1.6;">
            <p><b>1. Resim Seçimi:</b><br>
            Dosyalarınızı sürükleyip bırakın veya 'Dosya Seç' butonunu kullanın.</p>
            
            <p><b>2. İşlem Seçimi:</b></p>
            <ul style="margin-top: 0px; padding-left: 20px;">
                <li><b>Format Dönüştür:</b> Resimlerinizi JPG, PNG, WEBP, SVG gibi formatlara çevirin.</li>
                <li><b>Yeniden Boyutlandırma:</b> Genişlik/Yükseklik veya Yüzde olarak boyutlandırın.</li>
                <li><b>Kalite Artır:</b> Yapay zeka destekli algoritmalarla çözünürlüğü yükseltin.</li>
            </ul>
            
            <p><b>3. Başlat:</b><br>
            Tüm ayarları yaptıktan sonra 'İŞLEMİ BAŞLAT' butonuna basın.</p>
        </div>
        <p style="color: #a6adc8; font-style: italic; margin-top: 15px;">İpucu: 'Seçilen dosyaları temizle' butonu ile listenizi sıfırlayabilirsiniz.</p>
        """
        content.setText(html_content)
        layout.addWidget(content)

        layout.addStretch()

        # Footer
        footer = QLabel("Geliştirici : MYY Yazılım")
        footer.setObjectName("FooterLabel")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
