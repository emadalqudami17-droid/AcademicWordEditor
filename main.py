# main.py
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from utils.constants import (
    APP_NAME, FONT_ARABIC, FONT_ARABIC_BOLD,
)
from screens.home_screen import HomeScreen
from screens.editor_screen import EditorScreen
from screens.settings_screen import SettingsScreen


class AcademicWordApp(MDApp):

    def build(self):
        self.title = APP_NAME

        # تسجيل الخطوط العربية
        try:
            LabelBase.register(
                name="NotoNaskh",
                fn_regular=FONT_ARABIC,
                fn_bold=FONT_ARABIC_BOLD,
            )
            self.theme_cls.font_styles["NotoNaskh"] = [
                "NotoNaskh", 16, False, 0.15
            ]
        except Exception as e:
            print("Font register error:", e)

        # الثيم
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"

        # تحميل ملفات KV
        try:
            Builder.load_file("widgets/toolbar.kv")
            Builder.load_file("widgets/formatting_toolbar.kv")
        except Exception as e:
            print("KV load error:", e)

        # مدير الشاشات
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EditorScreen(name="editor"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm

    def on_start(self):
        Window.softinput_mode = "below_target"


if __name__ == "__main__":
    AcademicWordApp().run()