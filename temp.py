from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager

loader = """
<Screen1>:    
    name: 's1'
    MDRectangleFlatButton:
        id: btn
        text: "Connect"
        font_size: '18sp'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        on_release: app.server_connect()
"""

Builder.load_string(loader)

class Screen1(Screen):
    pass

class TempApp(MDApp):

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Screen1(name='s1'))

        return self.sm

    def server_connect(self):
        self.sm.get_screen('s1').ids.btn.text = "connected"

TempApp().run()