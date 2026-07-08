class UIStrings:
    """Centralized Turkish UI text. Not an i18n framework - just a single
    place to find/change every user-facing string in the app."""

    # --- Dosya Seçimi grubu ---
    GROUP_FILE_SELECTION = "1. Resim Seçimi"
    BTN_BROWSE = "Dosya Seç"
    LBL_SELECTED_FILES = "Seçilen Dosyalar:"
    BTN_CLEAR_FILES = "Seçilen dosyaları temizle"

    # --- İşlem Seçimi grubu ---
    GROUP_OPERATION = "2. İşlem Seçimi"
    OP_LABEL_CONVERT = "Format Dönüştür"
    OP_LABEL_RESIZE = "Yeniden Boyutlandırma"
    OP_LABEL_ENHANCE = "Kalite/Çözünürlük Artır"
    LBL_TARGET_FORMAT = "Hedef Format:"
    LBL_RESIZE_METHOD = "Yöntem:"
    RESIZE_METHOD_DIMENSIONS = "Boyut (px)"
    RESIZE_METHOD_PERCENT = "Yüzde (%)"
    LBL_WIDTH = "Genişlik:"
    LBL_HEIGHT = "Yükseklik:"
    LBL_PERCENT = "Oran (%):"
    LBL_ENHANCE_FACTOR = "Artış Çarpanı (x):"
    LBL_TARGET_FOLDER = "Hedef Klasör:"
    OUTPUT_PLACEHOLDER = "Varsayılan (Kaynak Klasör)"
    BTN_PROCESS = "İŞLEMİ BAŞLAT"

    # --- Dosya diyalogları ---
    DIALOG_SELECT_IMAGES_TITLE = "Resim Seç"
    DIALOG_IMAGE_FILTER = "Resim Dosyaları (*.png *.jpg *.jpeg *.bmp *.webp *.ico *.tiff *.svg)"
    DIALOG_SELECT_OUTPUT_FOLDER_TITLE = "Hedef Klasör Seç"

    # --- Durum çubuğu / işlem sonucu ---
    STATUS_READY = "Hazır"
    STATUS_COMPLETED = "İşlem Tamamlandı!"
    STATUS_ERROR_GENERIC = "Hata oluştu."
    STATUS_PARTIAL_ERROR_TEMPLATE = "{count} dosyada hata oluştu."
    MSG_WARNING_TITLE = "Uyarı"
    MSG_NO_FILES_SELECTED = "Lütfen önce dosya seçin!"
    MSG_PARTIAL_ERROR_TITLE = "Kısmi Hata"
    MSG_PARTIAL_ERROR_BODY_PREFIX = "Bazı dosyalar işlenemedi:\n\n"
    MSG_SUCCESS_TITLE = "Başarılı"
    MSG_SUCCESS_BODY = "Tüm işlemler tamamlandı."
    MSG_ERROR_TITLE = "Hata"

    # --- İkon bulunamazsa gösterilecek metin/emoji fallback'leri ---
    FALLBACK_INFO = "?"
    FALLBACK_BACK = "<-"
    FALLBACK_FOLDER = "📂"
    FALLBACK_REMOVE = "X"
    FALLBACK_THUMB_FILE = "📄"
    FALLBACK_THUMB_UNKNOWN = "?"
    FALLBACK_THEME_SUN = "☀️"
    FALLBACK_THEME_MOON = "🌙"

    # --- Dosya listesi öğesi: işlem durumu rozeti ---
    FILE_STATUS_PROCESSING = "⏳"
    FILE_STATUS_SUCCESS = "✅"
    FILE_STATUS_ERROR = "❌"

    # --- DropZone durum metinleri ---
    DROPZONE_DEFAULT_TEXT = "Resimleri Buraya Sürükleyin\nveya\nTıklayın"
    DROPZONE_DRAG_TEXT = "Bırak Gelsin! 📂"
    DROPZONE_UNSUPPORTED_TEXT = "Desteklenmeyen dosya türü ⚠️"

    # --- Tooltip'ler ---
    TOOLTIP_INFO = "Uygulama hakkında bilgi"
    TOOLTIP_THEME_TOGGLE_TO_LIGHT = "Açık temaya geç"
    TOOLTIP_THEME_TOGGLE_TO_DARK = "Koyu temaya geç"
    TOOLTIP_OUTPUT_SELECT = "Hedef klasör seç"
    TOOLTIP_REMOVE_FILE = "Listeden kaldır"
    TOOLTIP_DROPZONE = "Resim dosyalarını buraya sürükleyip bırakın veya tıklayarak seçin (Ctrl+O)"

    # --- Worker (arka plan işlem) mesaj şablonları ---
    WORKER_PROGRESS_TEMPLATE = "İşleniyor: {file}..."
    WORKER_ERROR_TEMPLATE = "Hata ({file}): {error}"
    WORKER_DONE = "Tamamlandı!"

    # --- Bilgi sayfası (InfoView) ---
    FOOTER_TEXT = "Geliştirici : MYY Yazılım"
    VERSION_TEMPLATE = "Versiyon: {version}"
    INFO_HTML_CONTENT = """
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
