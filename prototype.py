import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button, Label
from kivy.uix.togglebutton import ToggleButton

   
class Prototype(BoxLayout):
    instruments = ["Guitar", "Ukulele", "Mandolin", "Banjo"]
    songlist = None
    
    def build_songlist(self):
        self.songlist = []
    
        with open("songlist.txt", "r") as infile:
            for line in infile:
                match = re.match("^(.*)::(.*)\n$", line)
                self.songlist += [Button(text=match.group(1)+" ["+match.group(2)+"]", background_normal="icons/bg.png", text_size=[580, None], color=[0, 0, 0, 1], valign="middle", halign="left", on_click=self.song, font_size=24, size_hint_y=None, height=50)]
                
        self.songlist.sort(key=lambda btn: btn.text.capitalize())
        alpha = ""
        
        for btn in self.songlist:
            if btn.text[0].capitalize() != alpha:
                alpha = btn.text[0].capitalize()
                self.ids.songlist_view.add_widget(Label(text="", size_hint_y=None, height=20))
                self.ids.songlist_view.add_widget(Label(text=alpha, text_size=[580, None], valign="middle", halign="left", font_size=32, color=[0, 0, 0, 1], size_hint_y=None, height=50))
            self.ids.songlist_view.add_widget(btn)
        
        
    def record(self):
        # create new screens for the stop -> processing -> save
        pass


    def song(self, instance):
        pass


class PrototypeApp(App):
    def build(self):
        pt = Prototype()
        pt.build_songlist()
        return pt


if __name__ == "__main__":
    app = PrototypeApp()
    app.title = "SENG 310: High Fidelity Prototype"
    app.run()

