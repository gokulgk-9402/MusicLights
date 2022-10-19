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
        font_style: 'H4'
        halign: 'center'
    MDTextField:
        id: ipaddr
        multiline: False
        font_size: '30sp'
        padding: 10
        hint_text: "Enter IP address of Pi..."
        helper_text_mode: "on_focus"
        mode: "rectangle"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: 0.5, None
        height: '30sp'
        on_text_validate: app.server_connect(ipaddr.text)
    MDRectangleFlatButton:
        text: "Connect"
        font_size: '30sp'
        pos_hint: {'center_x':0.5, 'center_y':0.4}
        on_release: app.server_connect(ipaddr.text)

<Screen2>:
    name: 's2'
    MDBoxLayout:
        orientation: "vertical"
        MDToolbar:
            title: "Music Lights Control"
            elevation: 4
            left_action_items: [["chevron-left", lambda x: app.back_button()]]
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint: 0.85, None
            pos_hint: {'center_x':0.5}
            height: '60sp'
            MDLabel:
                id: disp
                text: "Off"
                size_hint: 0.7, 1
                font_style: 'H4'
            MDSwitch:
                id: onoff
                pos_hint: {'center_y':0.5}
                on_active: app.switchfun(self.active)
        MDFloatLayout:
            canvas:
                Color:
                    rgb: 0, 0, 0
                Rectangle:
                    size: self.size
                    pos: self.pos
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint: 0.7, None
                height: '20sp'
                pos_hint: {'center_x':0.5, 'center_y':0.85}
                Image:
                    source: 'bright-min.png'
                    size_hint: None, None
                    width: '70sp'
                    allow_stretch: True
                MDSlider:
                    id: bright
                    min: 0
                    max: 255
                    step: 1
                    size_hint: 1, None
                    on_touch_up: app.sendfun('bright', bright.value)
                Image:
                    source: 'bright-max.png'
                    size_hint: None, None
                    width: '70sp'
                    allow_stretch: True
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint: 0.7, None
                height: '20sp'
                pos_hint: {'center_x':0.5, 'center_y':0.7}
                Image:
                    source: 'mic-max.png'
                    size_hint: None, None
                    width: '70sp'
                    allow_stretch: True
                MDSlider:
                    id: sens
                    min: 0
                    max: 100
                    step: 1
                    size_hint: 1, None
                    on_touch_up: app.sendfun('sens', sens.value)
                Image:
                    source: 'mic-min.png'
                    size_hint: None, None
                    width: '70sp'
                    allow_stretch: True
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

    def server_connect(self, ipaddr):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER = ipaddr
        PORT = 5050
        self.client.settimeout(2)
        try:
            self.client.connect((SERVER, PORT))
            self.client.settimeout(None)
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
            self.sm.get_screen('s2').ids.bright.value = self.var_bright
            self.sm.get_screen('s2').ids.sens.value = self.var_sens * 100

        except:
            close_button = MDFlatButton(text = "CLOSE", on_release = self.c_err_btn)
            self.dialog1 = MDDialog(title = "Connection Error", text = "Couldn't connect to the Pi", size_hint = (0.7, 1), buttons = [close_button])
            self.dialog1.open()

    def c_err_btn(self, obj):
        self.dialog1.dismiss()
        return


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
            if val == self.var_bright:
                return
            self.sm.get_screen('s2').ids.bright.text = ""
            self.var_bright = val
            self.sm.get_screen('s2').ids.bright.helper_text = f"Current: {self.var_bright}"
        # elif attribute == 'status':
        #     self.sm.get_screen('s2').ids.status.text = ""
        elif attribute == 'sens':
            val = val / 100
            if val == self.var_sens:
                return
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
