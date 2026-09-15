# screens/editor_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivy.metrics import dp
from kivy.lang import Builder

from document.document_manager import Document
from utils.constants import (
    INSERT_MENU,
    ELEM_HEADING1, ELEM_HEADING2, ELEM_HEADING3,
)


KV = """
<EditorScreen>:
    md_bg_color: 1,1,1,1
    MDBoxLayout:
        orientation: "vertical"

        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            md_bg_color: app.theme_cls.primary_color
            padding: [dp(8), 0]

            MDIconButton:
                icon: "arrow-right"
                theme_text_color: "Custom"
                text_color: 1,1,1,1
                on_release: root.go_home()

            MDLabel:
                id: title_label
                text: "مستند جديد"
                theme_text_color: "Custom"
                text_color: 1,1,1,1
                halign: "right"

            MDIconButton:
                icon: "content-save"
                theme_text_color: "Custom"
                text_color: 1,1,1,1
                on_release: root.save_doc()

            MDIconButton:
                icon: "plus"
                theme_text_color: "Custom"
                text_color: 1,1,1,1
                on_release: root.open_insert_menu()

        MDBoxLayout:
            size_hint_y: None
            height: dp(48)
            md_bg_color: .95,.95,.95,1
            padding: [dp(6), 0]
            spacing: dp(2)

            MDIconButton:
                icon: "format-bold"
                on_release: root.fmt('bold')
            MDIconButton:
                icon: "format-italic"
                on_release: root.fmt('italic')
            MDIconButton:
                icon: "format-underline"
                on_release: root.fmt('underline')
            MDIconButton:
                icon: "format-header-1"
                on_release: root.h1()
            MDIconButton:
                icon: "format-header-2"
                on_release: root.h2()
            MDIconButton:
                icon: "format-align-right"
                on_release: root.align('right')
            MDIconButton:
                icon: "format-align-center"
                on_release: root.align('center')
            MDIconButton:
                icon: "format-align-left"
                on_release: root.align('left')
            MDIconButton:
                icon: "undo"
                on_release: root.undo()
            MDIconButton:
                icon: "redo"
                on_release: root.redo()

        MDScrollView:
            id: sv
            MDBoxLayout:
                id: content_box
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(6)
                size_hint_y: None
                height: self.minimum_height
"""


class EditorScreen(MDScreen):
    doc = None

    def load_document(self, doc):
        self.doc = doc
        self.ids.title_label.text = doc.title
        self.refresh()

    def refresh(self):
        box = self.ids.content_box
        box.clear_widgets()

        if not self.doc:
            return

        for e in self.doc.elements:
            if e.kind == ELEM_HEADING1:
                box.add_widget(MDLabel(
                    text=e.text,
                    halign="right",
                    font_style="H5",
                    size_hint_y=None,
                    height=dp(48),
                    theme_text_color="Primary",
                ))
            elif e.kind == ELEM_HEADING2:
                box.add_widget(MDLabel(
                    text=e.text,
                    halign="right",
                    font_style="H6",
                    size_hint_y=None,
                    height=dp(40),
                ))
            elif e.kind == ELEM_HEADING3:
                box.add_widget(MDLabel(
                    text=e.text,
                    halign="right",
                    font_style="Subtitle1",
                    size_hint_y=None,
                    height=dp(34),
                ))
            else:
                tf = MDTextField(
                    text=e.text,
                    multiline=True,
                    size_hint_y=None,
                    height=dp(80),
                    mode="rectangle",
                )
                tf.bind(
                    text=lambda inst, val, el=e: setattr(el, "text", val)
                )
                box.add_widget(tf)

    # ---------- أدوات ----------
    def go_home(self):
        self.save_doc(silent=True)
        self.manager.current = "home"

    def save_doc(self, silent=False):
        if self.doc:
            self.doc.save()
            if not silent:
                toast("تم الحفظ")

    def fmt(self, kind):
        toast(f"تنسيق: {kind}")

    def h1(self):
        if self.doc:
            self.doc.add_heading("عنوان جديد", 1)
            self.refresh()

    def h2(self):
        if self.doc:
            self.doc.add_heading("عنوان فرعي", 2)
            self.refresh()

    def align(self, a):
        toast(f"محاذاة: {a}")

    def undo(self):
        toast("تراجع")

    def redo(self):
        toast("إعادة")

    def open_insert_menu(self):
        from kivymd.uix.bottomsheet import MDListBottomSheet
        bs = MDListBottomSheet()
        for icon, title, key in INSERT_MENU:
            bs.add_item(
                title,
                lambda x, k=key: self._insert(k),
                icon=icon,
            )
        bs.open()

    def _insert(self, key):
        if not self.doc:
            return
        if key == "toc":
            self._insert_toc()
        elif key == "list_figures":
            self._insert_list("figure")
        elif key == "list_tables":
            self._insert_list("table")
        elif key == "page_break":
            self.doc.add_page_break()
            self.refresh()
        elif key == "section_break":
            self.doc.add_section_break()
            self.refresh()
        elif key == "image":
            toast("اختيار صورة - لاحقًا")
        else:
            toast(f"إدراج: {key}")

    def _insert_toc(self):
        heads = self.doc.get_headings()
        if not heads:
            toast("لا توجد عناوين")
            return
        self.doc.add_heading("جدول المحتويات", 1)
        for i, h in enumerate(heads, 1):
            level = h.meta.get("level", 1)
            prefix = "    " * (level - 1)
            self.doc.add_paragraph(f"{prefix}{i}. {h.text}")
        self.refresh()
        toast("تم توليد جدول المحتويات")

    def _insert_list(self, kind):
        caps = self.doc.get_captions(kind)
        title = "قائمة الأشكال" if kind == "figure" else "قائمة الجداول"
        self.doc.add_heading(title, 1)
        if not caps:
            self.doc.add_paragraph("(لا توجد عناصر)")
        else:
            for c in caps:
                self.doc.add_paragraph(c.text)
        self.refresh()


Builder.load_string(KV)