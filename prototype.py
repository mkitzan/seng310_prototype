import re
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button, Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen

   
class Landing(Screen):
    def build_songlist(self):
        self.remove_widget(self.ids.songlist_view)
        songlist = []
    
        with open("songlist.txt", "r") as infile:
            for line in infile:
                match = re.match("^(.*)::(.*)\n$", line)
                songlist += [Button(text=match.group(1)+" ["+match.group(2)+"]", background_normal="icons/bg.png", text_size=[580, None], color=[0, 0, 0, 1], \
                                         valign="middle", halign="left", on_click=self.song, font_size=24, size_hint_y=None, height=50)]
                
        songlist.sort(key=lambda btn: btn.text.capitalize())
        alpha = ""
        
        for btn in songlist:
            if btn.text[0].capitalize() != alpha:
                alpha = btn.text[0].capitalize()
                self.ids.songlist_view.add_widget(Label(text="", size_hint_y=None, height=20))
                self.ids.songlist_view.add_widget(Label(text=alpha, text_size=[580, None], valign="middle", halign="left", font_size=32, color=[0, 0, 0, 1], size_hint_y=None, height=50))
            self.ids.songlist_view.add_widget(btn)
          
            
    def song():
        pass
        
        
class Record(Screen):
    hold = None
    
    def reset(self):
        if self.hold is not None:
            self.ids.grid.remove_widget(self.ids.grid.children[0])
            self.ids.grid.add_widget(self.hold)
        
        self.ids.element.background_normal="icons/stop-normal.png"
        self.ids.element.background_down="icons/stop-down.png"


    def pressed(self):
        if self.ids.element.background_normal == "icons/stop-normal.png":
            self.ids.element.background_normal="icons/buffer.png"
            self.ids.element.background_down="icons/buffer.png"
        else:
            self.hold = self.ids.element
            self.ids.grid.remove_widget(self.ids.grid.children[0])
            self.ids.grid.add_widget(SaveInput())
            
        
class Song(Screen):
    pass
    
    
class SaveInput(BoxLayout):
    pass
    

class PrototypeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Landing(name="landing"))
        sm.children[0].build_songlist()
        sm.add_widget(Record(name="record"))
        
        return sm


if __name__ == "__main__":
    app = PrototypeApp()
    app.title = "SENG 310: High Fidelity Prototype"
    app.run()

