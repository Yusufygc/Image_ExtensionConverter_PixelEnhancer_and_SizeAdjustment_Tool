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
