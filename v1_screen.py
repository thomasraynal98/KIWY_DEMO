from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

screen_helper="""
ScreenManager:
    BaseDisconnected:

<BaseDisconnected>:
    name: 'screen1'
    MDFloatLayout:
        md_bg_color: 0.129, 0.586, 0.949, 1
        
        MDLabel:
            text:'CONNEXION INTERROMPUE'
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
            pos_hint: {"center_x":0.5,"center_y":0.43}
"""

def change_screen(self,screen_name):
    self.manager.current = screen_name
    
class BaseDisconnected(Screen):
    pass

class V1_screenApp(MDApp):
    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen

if __name__ == "__main__":
    sm = ScreenManager()
    sm.add_widget(BaseDisconnected(name='screen1'))

    Window.size = (1024, 600)
    V1_screenApp().run()