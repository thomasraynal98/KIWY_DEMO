from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
import redis

import os
import requests
os.environ["KIVY_WINDOW"] = "egl_rpi"
os.environ["KIVY_GL_BACKEND"] = "gl"

r = redis.Redis(host='localhost', port=6379, db=0)

screen_helper="""
ScreenManager:
    BaseDisconnected:
    BaseConnected:

<BaseDisconnected>:
    name: 'screen1'
    MDFloatLayout:
        md_bg_color: 0.54, 0.16, 0.88, 1
        
        MDLabel:
            text:'BASE NO DETECTED'
            halign:'center'
            font_style:'Button'
            font_size:60
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            padding: (10,10)
            pos_hint:{"center_x":0.5,"center_y":0.57}
        
        MDIconButton:
            icon: 'message-alert'
            user_font_size: "150sp"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            pos_hint: {"center_x":0.5,"center_y":0.35}

<BaseConnected>:
    name: 'screen2'
    MDFloatLayout:
        md_bg_color: 0, 1, 0.49, 1
        
        MDLabel:
            text:'NEW BASE DETECTED'
            halign:'center'
            font_style:'Button'
            font_size:60
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            padding: (10,10)
            pos_hint:{"center_x":0.5,"center_y":0.57}

        MDLabel:
            text: pipi
            halign:'center'
            font_style:'Button'
            font_size:60
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            padding: (10,10)
            pos_hint:{"center_x":0.8,"center_y":0.8}
        
        MDIconButton:
            icon: 'check-decagram'
            user_font_size: "150sp"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            pos_hint: {"center_x":0.5,"center_y":0.35}
"""

def change_screen(self,screen_name):
    self.manager.current = screen_name
    
class BaseConnected(Screen):
    # State_base_identifiant = ObjectProperty(str((r.get('State_base_identifiant')).decode('utf-8')))

    def read_redis(self,dt):
        # self.ids.lbl1.text = (r.get('State_base_identifiant')).decode('utf-8')
        connection = r.get('State_connection_base')
        connection_s = connection.decode('utf-8')

        if(connection_s == "DISCONNECTED"):
            change_screen(self, 'screen1')

        elif(connection_s == "CONNECTED"):
            change_screen(self, 'screen2')
    
    def on_enter(self, *args):
        # State_base_identifiant = ObjectProperty(str((r.get('State_base_identifiant')).decode('utf-8')))
        Clock.schedule_interval(self.read_redis, 1)

class BaseDisconnected(Screen):
    def read_redis(self,dt):
        connection = r.get('State_connection_base')
        connection_s = connection.decode('utf-8')

        if(connection_s == "DISCONNECTED"):
            change_screen(self, 'screen1')

        elif(connection_s == "CONNECTED"):
            change_screen(self, 'screen2')
    
    def on_enter(self, *args):
        # self.State_base_identifiant = ObjectProperty(str((r.get('State_base_identifiant')).decode('utf-8')))
        Clock.schedule_interval(self.read_redis, 1)

class V1_screenApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


sm = ScreenManager()
sm.add_widget(BaseDisconnected(name='screen1'))
sm.add_widget(BaseConnected(name='screen2'))

Window.size = (1024, 600)
V1_screenApp().run()