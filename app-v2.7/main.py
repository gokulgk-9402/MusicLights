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
    Image:
        source: 'img.png'
        size_hint_x: 0.4
        allow_stretch: True
        pos_hint: {'center_x':0.5, 'center_y':0.75}
    MDLabel:
        text: "Music Lights"
        pos_hint: {'center_x':0.5, 'center_y':0.6}
        size_hint: 0.6, 0.2
        font_style: 'H2'
        halign: 'center'
    MDRectangleFlatButton:
        text: "Connect"
        font_size: '30sp'
        pos_hint: {'center_x':0.5, 'center_y':0.45}
        on_release: app.server_connect()

<Screen2>:
    name: 's2'
    MDLabel:
        id: disp
        text: "Off"
        pos_hint: {'center_x':0.5, 'center_y':0.95}
        size_hint: 0.6, 0.2
        font_style: 'H4'
    MDFloatingActionButton:
        icon: "arrow-left-bold"
        pos_hint: {'center_x': 0.1, 'center_y':0.95}
        on_release: app.back_button()
    MDSwitch:
        id: onoff
        pos_hint: {'center_x':0.9, 'center_y':0.95}
        on_active: app.switchfun(self.active)
    MDTextField:
        id: bright
        multiline: False
        font_size: '30sp'
        padding: 10
        hint_text: "Enter brightness..."
        helper_text_mode: "on_focus"
        mode: "rectangle"
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        size_hint: 0.5, None
        height: '30sp'
        on_text_validate: app.sendfun('bright', bright.text)
    MDFloatingActionButton:
        icon: "send"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        on_release: app.sendfun('bright', bright.text)
    MDTextField:
        id: sens
        multiline: False
        font_size: '30sp'
        padding: 10
        hint_text: "Enter Sensitivity..."
        helper_text_mode: "on_focus"
        mode: "rectangle"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint: 0.5, None
        height: '30sp'
        on_text_validate: app.sendfun('sens', sens.text)
    MDFloatingActionButton:
        icon: "send"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
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
        
        self.send_message("!cur status")
        self.var_status = self.recv_message()
        self.send_message("!cur brightness")
        self.var_bright = int(self.recv_message())
        self.send_message("!cur sens")
        self.var_sens = float(self.recv_message())

        self.root.current = 's2'

        if self.var_status == 'on':
            self.sm.get_screen('s2').ids.onoff.active = True
            self.sm.get_screen('s2').ids.disp.text = 'On'

        print(self.var_bright, self.var_sens)
        self.sm.get_screen('s2').ids.bright.helper_text = f"Current: {self.var_bright}"
        self.sm.get_screen('s2').ids.sens.helper_text = f"Current: {self.var_sens}"


    def send_message(self, message):
        msg = message.encode('utf-8')
        msg_len = len(msg)
        send_len = str(msg_len).encode('utf-8')
        send_len += b' ' * (64 - len(send_len))
        self.client.send(send_len)
        self.client.send(msg)

    def recv_message(self):
        msg_length = self.client.recv(64).decode('utf-8')
        msg_length = int(msg_length)
        message = self.client.recv(msg_length).decode('utf-8')
        return message

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
            self.sm.get_screen('s2').ids.bright.text = ""
            self.var_bright = int(val)
            self.sm.get_screen('s2').ids.bright.helper_text = f"Current: {self.var_bright}"
        # elif attribute == 'status':
        #     self.sm.get_screen('s2').ids.status.text = ""
        elif attribute == 'sens':
            self.sm.get_screen('s2').ids.sens.text = ""
            self.var_sens = float(val)
            self.sm.get_screen('s2').ids.sens.helper_text = f"Current: {self.var_sens}"

        self.send_message(f'!{attribute} {val}')

    def switchfun(self, on):
        if on:
            self.send_message("!status on")
            self.sm.get_screen('s2').ids.disp.text = 'On'
        else:
            self.send_message("!status off")
            self.sm.get_screen('s2').ids.disp.text = 'Off'

    def on_stop(self):
        print("App closed")
        if self.root.current == 's2':
            self.back_button()

MusicLightsApp().run()
