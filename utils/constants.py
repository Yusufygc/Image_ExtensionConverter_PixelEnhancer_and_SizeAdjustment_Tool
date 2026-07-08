class AppConstants:
    APP_NAME = "Uzantı Dönüştürücü ve Piksel Artırıcı"
    VERSION = "1.0.0"
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    
    # Desteklenen Formatlar
    SUPPORTED_FORMATS = [
        "JPEG", "PNG", "WEBP", "BMP", "ICO", "TIFF", "SVG"
    ]

    # Sürükle-bırak / dosya seçimi için desteklenen uzantılar
    SUPPORTED_EXTENSIONS = [
        ".png", ".jpg", ".jpeg", ".bmp", ".webp", ".ico", ".tiff", ".svg"
    ]
    
    # Varsayılan değerler
    DEFAULT_QUALITY = 90
    ENHANCED_QUALITY = 95
    DEFAULT_OUTPUT_FOLDER = "Converted_Images"


class AppIcons:
    APP = "assets/icons/icon.ico"
    UPLOAD = "assets/icons/upload_icon.svg"
    DELETE = "assets/icons/delete_icon.svg"
    INFO = "assets/icons/info_icon.svg"
    FOLDER = "assets/icons/folder_icon.svg"
    FILE = "assets/icons/file_icon.svg"
    BACK_ARROW = "assets/icons/back_arrow.svg"
    DOWN_ARROW = "assets/icons/down-arrow.svg"
    UP_ARROW = "assets/icons/up-arrow.svg"
    MAIN_QSS = "assets/style/main.qss"
