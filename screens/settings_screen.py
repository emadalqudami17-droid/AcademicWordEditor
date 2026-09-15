# screens/settings_screen.py
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder


KV = """
<SettingsScreen>:
    md_bg_color: app.theme_cls.bg_light
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "الإعدادات"
            left_action_items: [["arrow-right", lambda x: root.go_home()]]

        MDBoxLayout:
            padding: dp(20)

            MDLabel:
                text: "الإعدادات ستضاف هنا"
                halign: "center"
"""


class SettingsScreen(MDScreen):
    def go_home(self):
        self.manager.current = "home"


Builder.load_string(KV)