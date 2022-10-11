from time import sleep
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

import socket

# from kivy.core.window import Window

# Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
# Window.softinput_mode = "below_target"

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

loader = """
<Screen1>:    
    name: 's1'
    MDRectangleFlatButton:
        text: "Connect"
        font_size: '18sp'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        on_release: app.server_connect()

<Screen2>:
    name: 's2'
    MDFloatingActionButton:
        icon: "arrow-left-bold"
        pos_hint: {'center_x': 0.1, 'center_y':0.9}
        on_release: app.back_button()
    MDTextField:
        id: bright
        multiline: False
        font_size: '30sp'
        padding: 10
        hint_text: "Enter Command..."
        mode: "rectangle"
        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
        size_hint: 0.5, None
        height: '35sp'
        on_text_validate: app.sendfun('bright', bright.text)
    MDFloatingActionButton:
        icon: "send"
        pos_hint: {'center_x': 0.5, 'center_y': 0.65}
        on_release: app.sendfun('bright', bright.text)
    MDTextField:
        id: sens
        multiline: False
        font_size: '30sp'
        padding: 10
        hint_text: "Enter Command..."
        mode: "rectangle"
        pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        size_hint: 0.5, None
        height: '35sp'
        on_text_validate: app.sendfun('sens', sens.text)
    MDFloatingActionButton:
        icon: "send"
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        on_release: app.sendfun('sens', sens.text)
"""

Builder.load_string(loader)

class Screen1(Screen):
    pass

class Screen2(Screen):
    pass


class MusicLightsApp(MDApp):

    def build(self):
        self.icon = "icon.png"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.sm = ScreenManager()
        self.sm.add_widget(Screen1(name = 's1'))
        self.sm.add_widget(Screen2(name = 's2'))

        return self.sm

    def server_connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER = "192.168.1.204"
        PORT = 5050
        self.client.connect((SERVER, PORT))
        print("Connected to server!")
        self.root.current = 's2'

    def send_message(self, message):
        msg = message.encode('utf-8')
        msg_len = len(msg)
        send_len = str(msg_len).encode('utf-8')
        send_len += b' ' * (64 - len(send_len))
        self.client.send(send_len)
        self.client.send(msg)
        # self.sm.get_screen('s2').ids.message.text = ""

    def back_button(self):
        self.send_message("!DC")
        close_button = MDFlatButton(text = "CLOSE", on_release = self.dc_btn)
        self.dialog2 = MDDialog(title = "Disconnected", text = "Disconnected from the Server", size_hint = (0.7, 1), buttons = [close_button])
        self.dialog2.open()
        sleep(1)
        self.client.close()
    
    def dc_btn(self, obj):
        self.dialog2.dismiss()
        self.root.current = 's1'
        return

    def sendfun(self, attribute, val):
        if attribute == 'bright':
            if int(val) == self.bright:
                return
            self.send_message(f'!{attribute} {val}')
            self.bright = int(val)
            self.sm.get_screen('s2').ids.bright.helper_text = f"Current: {self.bright}"
        else:
            if float(val) == self.sens:
                return
            self.send_message(f'!{attribute} {val}')
            self.sens = float(val)
            self.sm.get_screen('s2').ids.sens.helper_text = f"Current: {self.sens}"


    def on_stop(self):
        print("App closed")
        if self.root.current == 's2':
            self.back_button()

MusicLightsApp().run()
