# screens/home_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.lang import Builder

from document.document_manager import Document


KV = """
<HomeScreen>:
    md_bg_color: app.theme_cls.bg_light
    MDBoxLayout:
        orientation: "vertical"

        MDBoxLayout:
            size_hint_y: None
            height: dp(160)
            orientation: "vertical"
            padding: dp(16)
            md_bg_color: app.theme_cls.primary_color

            MDLabel:
                text: "Academic Word"
                halign: "center"
                font_style: "H4"
                theme_text_color: "Custom"
                text_color: 1,1,1,1

            MDLabel:
                text: "محرر أكاديمي عربي"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1,1,1,.75

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(14)

            MDRaisedButton:
                text: "مستند جديد"
                icon: "file-plus"
                size_hint_x: 1
                size_hint_y: None
                height: dp(56)
                on_release: root.new_document()

            MDRaisedButton:
                text: "فتح مستند"
                icon: "folder-open"
                size_hint_x: 1
                size_hint_y: None
                height: dp(56)
                on_release: root.show_recent()

            MDRaisedButton:
                text: "المستندات الأخيرة"
                icon: "history"
                size_hint_x: 1
                size_hint_y: None
                height: dp(56)
                on_release: root.show_recent()

            MDRaisedButton:
                text: "الإعدادات"
                icon: "cog"
                size_hint_x: 1
                size_hint_y: None
                height: dp(56)
                on_release: root.go_settings()
"""


class HomeScreen(MDScreen):
    dialog = None

    def new_document(self):
        doc = Document(title="مستند جديد")
        doc.add_heading("المقدمة", 1)
        doc.add_paragraph("ابدأ الكتابة هنا...")
        doc.save()

        editor = self.manager.get_screen("editor")
        editor.load_document(doc)
        self.manager.current = "editor"

    def show_recent(self):
        docs = Document.list_documents()
        if not docs:
            self._toast("لا توجد مستندات محفوظة")
            return

        items = MDList()
        for d in docs:
            it = OneLineAvatarIconListItem(text=d["title"])
            it.add_widget(IconLeftWidget(icon="file-document-outline"))
            it.bind(
                on_release=lambda x, did=d["id"]: self._open(did)
            )
            items.add_widget(it)

        self.dialog = MDDialog(
            title="المستندات الأخيرة",
            type="custom",
            content_cls=items,
            buttons=[],
        )
        self.dialog.open()

    def _open(self, doc_id):
        if self.dialog:
            self.dialog.dismiss()
        doc = Document.load(doc_id)
        editor = self.manager.get_screen("editor")
        editor.load_document(doc)
        self.manager.current = "editor"

    def go_settings(self):
        self.manager.current = "settings"

    def _toast(self, msg):
        from kivymd.toast import toast
        toast(msg)


Builder.load_string(KV)