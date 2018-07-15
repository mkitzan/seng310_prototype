import re
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.button import Button, Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen

SM = None
songlist_file = "songlist.txt"
   
   
class Landing(Screen):
    def build_songlist(self):
        self.ids.songlist_view.clear_widgets()
        songlist = []
    
        with open(songlist_file, "r") as infile:
            for line in infile:
                match = re.match("^(.*)::(.*)\n$", line)
                songlist += [Button(text=match.group(1)+" ["+match.group(2)+"]", background_normal="icons/song-normal.png", background_down="icons/song-down.png", \
                             text_size=[580, None], color=[0, 0, 0, 1], valign="middle", halign="left", on_press=self.song, font_size=24, size_hint_y=None, height=50)]
                
        songlist.sort(key=lambda btn: btn.text.capitalize())
        alpha = ""
        
        for btn in songlist:
            if btn.text[0].capitalize() != alpha:
                alpha = btn.text[0].capitalize()
                self.ids.songlist_view.add_widget(Label(text="", size_hint_y=None, height=20))
                self.ids.songlist_view.add_widget(Label(text=alpha, text_size=[580, None], valign="middle", halign="left", font_size=32, color=[0, 0, 0, 1], size_hint_y=None, height=50))
            self.ids.songlist_view.add_widget(btn)
          
            
    def song(self, instance):
        match = re.match("^(.*) \[(.*)\]$", instance.text)
        self.manager.transition.direction = "left"
        self.manager.current = "song"
        SM.children[0].set_header(match.group(1), match.group(2))
        SM.children[0].build_song()
        
        
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
    def set_header(self, title, instr):
        self.ids.title.text = title
        self.ids.instr.text = instr
        self.notes = [[]]
        self.beats = [[]]
        self.red = [.96, .03, .03, 1]
    
    
    def build_song(self):
        sources = {"u": "icons/arrow-up-black.png", "d": "icons/arrow-down-black.png"}
        line_len = 16;
        count = 0
        space = 1/(line_len-2)
        
        with open("songs/"+self.ids.title.text.replace(" ", "-")+".txt", "r") as infile:
            for line in infile:
                match = re.match("^\[(.*)\]([d|u]*)\n$", line)
                start = True
                
                for ch in match.group(2):
                    if count == line_len:
                        self.beats += [[]]
                        self.notes += [[]]
                        count = 0
                        
                    if count == 0 or start == True:
                        self.notes[-1] += [Label(text=match.group(1), font_size=38, color=[0, 0, 0, 1], size_hint=[space, None], height=50, bold=True), -1]
                        start = False
                        
                    self.beats[-1] += [Image(source=sources[ch], size_hint=[space, None], height=28)]
                    self.notes[-1][-1] += 1
                    count += 1
                    
                self.beats[-1] += [Label(text="", size_hint=[space, None], height=28)]
                self.notes[-1] += [Label(text="", size_hint=[space, None], height=28)]

        self.beats[0][0].source = self.beats[0][0].source.replace("black", "red")
        self.notes[0][0].color = self.red
        
        for i in range(len(self.notes)):
            self.ids.sheetmusic.add_widget(Label(text="", size_hint_y=None, height=28))
            
            top_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
            bot_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=28)
            
            bot_layout.add_widget(Label(text="", size_hint=[space, None], height=28))
            top_layout.add_widget(Label(text="", size_hint=[space, None], height=28))
            
            for j in range(len(self.notes[i])):
                if type(self.notes[i][j]) is int:
                    top_layout.add_widget(Label(text="", size_hint=[space*self.notes[i][j], None], height=50))
                else:
                    top_layout.add_widget(self.notes[i][j])
            for el in self.beats[i]:
                bot_layout.add_widget(el)
                
            self.ids.sheetmusic.add_widget(top_layout)
            self.ids.sheetmusic.add_widget(bot_layout)
            
    
class SaveInput(BoxLayout):
    def save_song(self, spinner_loc):
        with open(songlist_file, "a") as outfile:
            outfile.write(self.ids.songname.text+"::"+spinner_loc.ids.dropdown.text+"\n")
        SM.children[0].build_songlist()
    

class PrototypeApp(App):
    def build(self):
        global SM
        SM = ScreenManager()
        SM.add_widget(Landing(name="landing"))
        SM.children[0].build_songlist()
        SM.add_widget(Record(name="record"))
        SM.add_widget(Song(name="song"))
        
        return SM


if __name__ == "__main__":
    app = PrototypeApp()
    app.title = "SENG 310: High Fidelity Prototype"
    app.run()

