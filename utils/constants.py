# utils/constants.py

APP_NAME = "Academic Word Editor"
APP_VERSION = "0.1.0"

# المسارات
FONT_ARABIC = "assets/fonts/NotoNaskhArabic-Regular.ttf"
FONT_ARABIC_BOLD = "assets/fonts/NotoNaskhArabic-Bold.ttf"
DATA_DIR = "data/documents"
BACKUP_DIR = "data/backups"
TEMPLATES_DIR = "data/templates"

# الألوان
COLOR_PRIMARY = "#37474F"
COLOR_BG = "#F5F5F5"
COLOR_SURFACE = "#FFFFFF"
COLOR_ACCENT = "#1976D2"
COLOR_TEXT = "#212121"
COLOR_MUTED = "#757575"

# أنواع عناصر المستند
ELEM_HEADING1 = "heading1"
ELEM_HEADING2 = "heading2"
ELEM_HEADING3 = "heading3"
ELEM_PARAGRAPH = "paragraph"
ELEM_FIGURE = "figure"
ELEM_CAPTION = "caption"
ELEM_TABLE = "table"
ELEM_SECTION = "section_break"
ELEM_PAGEBREAK = "page_break"

# قائمة الإدراج
INSERT_MENU = [
    ("\U0001F4C4", "جدول المحتويات", "toc"),
    ("\U0001F4CA", "قائمة الجداول", "list_tables"),
    ("\U0001F5BC", "قائمة الأشكال", "list_figures"),
    ("\U0001F4F7", "صورة", "image"),
    ("\U0001F4DD", "شرح توضيحي", "caption"),
    ("\U0001F4CB", "جدول", "table"),
    ("\u2797", "معادلة", "equation"),
    ("\U0001F517", "رابط", "link"),
    ("\U0001F516", "إشارة مرجعية", "bookmark"),
    ("\U0001F504", "مرجع متقاطع", "crossref"),
    ("\U0001F4DD", "حاشية سفلية", "footnote"),
    ("\U0001F4D1", "حاشية ختامية", "endnote"),
    ("\u2500", "فاصل صفحات", "page_break"),
    ("\u2551", "فاصل مقاطع", "section_break"),
    ("\U0001F522", "رقم الصفحة", "page_number"),
    ("\U0001F4D1", "رأس الصفحة", "header"),
    ("\U0001F4D1", "تذييل الصفحة", "footer"),
]