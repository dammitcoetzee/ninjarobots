# Gerrit Coetzee 2018
#Forgive me father for all I wanted was a cross-platform TUI Library and as punishment asciimatics was bestowed unto me
#sciimatics is a wasteland and this is hacked together by ignoring the documentation entirely.
# #goodluck.

#this library makes me feel like a fucking crazy person. 

from asciimatics.paths import Path, DynamicPath
from asciimatics.screen import Screen
from asciimatics.scene import Scene

from asciimatics.effects import Sprite, Print
from asciimatics.renderers import StaticRenderer, DynamicRenderer, Rainbow
from asciimatics.event import KeyboardEvent

import time
import re

selection = " "
timer = time.time()
current_menu_message = ["Which servo is moving? ","    ","    "]


def generate_scroller_frames():
    scroller = [
        " ███▄    █  ██▓ ███▄    █  ▄▄▄██▀▀▀▄▄▄          ██▀███   ▒█████   ▄▄▄▄    ▒█████  ▄▄▄█████▓▒███████▒   ",
        " ██ ▀█   █ ▓██▒ ██ ▀█   █    ▒██  ▒████▄       ▓██ ▒ ██▒▒██▒  ██▒▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒▒ ▒ ▒ ▄▀░   ",
        "▓██  ▀█ ██▒▒██▒▓██  ▀█ ██▒   ░██  ▒██  ▀█▄     ▓██ ░▄█ ▒▒██░  ██▒▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░░ ▒ ▄▀▒░    ",
        "▓██▒  ▐▌██▒░██░▓██▒  ▐▌██▒▓██▄██▓ ░██▄▄▄▄██    ▒██▀▀█▄  ▒██   ██░▒██░█▀  ▒██   ██░░ ▓██▓ ░   ▄▀▒   ░   ",
        "▒██░   ▓██░░██░▒██░   ▓██░ ▓███▒   ▓█   ▓██▒   ░██▓ ▒██▒░ ████▓▒░░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ ▒███████▒   ",
        "░ ▒░   ▒ ▒ ░▓  ░ ▒░   ▒ ▒  ▒▓▒▒░   ▒▒   ▓▒█░   ░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   ░▒▒ ▓░▒░▒   ",
        "░ ░░   ░ ▒░ ▒ ░░ ░░   ░ ▒░ ▒ ░▒░    ▒   ▒▒ ░     ░▒ ░ ▒░  ░ ▒ ▒░ ▒░▒   ░   ░ ▒ ▒░     ░    ░░▒ ▒ ░ ▒   ",
        "   ░   ░ ░  ▒ ░   ░   ░ ░  ░ ░ ░    ░   ▒        ░░   ░ ░ ░ ░ ▒   ░    ░ ░ ░ ░ ▒    ░      ░ ░ ░ ░ ░   ",
        "         ░  ░           ░  ░   ░        ░  ░      ░         ░ ░   ░          ░ ░             ░ ░       ",
        "Gerrit Coetzee 2018 | Version 1.0 | Confurator-O-Matic                 ░                   ░           ",
    ]

    scroller_animation = []
    scroller_len = len(scroller[0])
    scrolling_animation_width = 40

    scroller_segment_height = len(scroller)//5
    scroller_colors = []
    color_count = 0
    # This was where I tried to make a cool gradient for a while until I realized windows doesn't support 256 colors!
    # I aslo considered urwid for a bit but then there's some fuckery with cygwin or other garbage and I didn't wanna
    # I also don't want to upen up a VM yet because I don't. 
    for _ in scroller:
        # COLOUR_BLACK = 0
        # COLOUR_RED = 1
        # COLOUR_GREEN = 2
        # COLOUR_YELLOW = 3
        # COLOUR_BLUE = 4
        # COLOUR_MAGENTA = 5
        # COLOUR_CYAN = 6
        # COLOUR_WHITE = 7
        if color_count < scroller_segment_height:  # top
            scroller_colors.append("${1}")
        elif (color_count > scroller_segment_height*2):  # bottom
            scroller_colors.append("${1}")
        else:
            scroller_colors.append("${1}")  # middle
        color_count += 1

    #     print(scroller_colors)

    for j in range(0, scroller_len):  # this creates a looping frame set for the length of the art
        frame = ""
        color_shift = 0
        for k in scroller:
            frame += scroller_colors[color_shift]
            end = j+scrolling_animation_width
            if end >= scroller_len:
                end = end - scroller_len
                frame += k[j:scroller_len-1]
                frame += k[0:end]
            else:
                frame += k[j:end]
            frame += "\n"
            color_shift += 1
        # print(frame)

        scroller_animation.append(frame)
    return scroller_animation


class NinjaRobotScroller(Sprite):
    def __init__(self, screen, path, start_frame=0, stop_frame=0):

        super().__init__(
            screen,
            renderer_dict={"default": StaticRenderer(
                images=generate_scroller_frames())},
            path=path,

        )

        def _update(self, frame_no):
            super(NinjaRobotScroller, self)._update(frame_no)


class SelectorBox(DynamicRenderer):
    def __init__(self, number):
        self._height = 3
        self._width = 11
        super().__init__(self._height, self._width)
        self._number = number
        labels = [
            "LF Foot",
            "LF Base",
            "RF Foot",
            "RF Base",
            "LR Base",
            "LR Foot",
            "RR Base",
            "RR Foot",
        ]
        self._label = labels[self._number-1]
        self._selected = False
        self._frame_top = "[{0}]--------+    ".format(number)
        self._frame_mid = "| {0} |            ".format(self._label)
        self._frame_base = "+---------+    "

    def _render_now(self):
        x = 0
        for i in range(0, self._width):
            self._write(self._frame_top[i], x, 0)
            x += 1
        x = 0
        for i in range(0, self._width):
            if i > 1 and i < 10:
                if selection == self._number:
                    self._write(self._frame_mid[i],
                                x, 1, colour=7, bg=4, attr=1)
                else:
                    self._write(self._frame_mid[i], x, 1, attr=1)
            else:
                self._write(self._frame_mid[i], x, 1)
            x += 1
        x = 0
        for i in range(0, self._width):
            self._write(self._frame_base[i], x, 2)
            x += 1

        return self._plain_image, self._colour_map


# --- Menu and App Logic Below


class NinjaMenu(DynamicRenderer):
    def __init__(self):
        super().__init__(4, 50)
        self._color_esc_code = r"^\$\{((\d+),(\d+),(\d+)|(\d+),(\d+)|(\d+))\}(.*)"
        self._color_sequence = re.compile(self._color_esc_code)
        self._last_message = current_menu_message

    def _render_now(self):
        global current_menu_message
        # for i in self._last_message:
        #     y = 0
        #     writemessage = " " 
        #     for j in range(0,len(i)):
        #         writemessage+= "#"
        #     self._write(writemessage,x=0,y=y,colour=7,bg=1)
        #     y+=1
        # for i in range(0,len(self.images)):
        #     self.images[i]="  "
        
        self._last_message = current_menu_message
        # for z in range (0,2):
        #     self._write( "                                               ",0,int(z)
        y = 0
        for i in current_menu_message:
            # Regular expression for use to find colour sequences in multi-colour text.
            # It should match ${n}, ${m,n} or ${m,n,o}
        

            match = self._color_sequence.match(i)
            # print(match)
            i = i.split(';')

            if match is None:
                self._write(i[0], 0, y)
            else:
                attributes = (int(match.group(2)),
                            int(match.group(3)),
                            int(match.group(4)))
                self._write(i[0][match.start()+8:], 0, y,
                            colour=attributes[0], attr=attributes[1], bg=attributes[2])

            try:
                extramessage = i[1]
                print(i[0])
                self._write(extramessage, len(
                    i[0].lstrip(' \n\t'))+1, y, colour=0, attr=2, bg=3)

            except:
                pass

            y += 1
        return self._plain_image, self._colour_map

class KeyboardLogic(Sprite):
    def __init__(self, screen):
        images = [""]
        super().__init__(
            screen,
            renderer_dict={"default": StaticRenderer(
                images=images)},
            path=KeyboardController(screen, 0,0) #goddamn fucking seriously what the fucking fuck is this garbage?
            # I mean all I want to do is get keyboard input and I have to fucking make a fucking invisible magic sprite
            # pass it to a "renderer" and then it gets in some sort of magic loop some fucking where and now I can 
            # fucking handle the fucking code I DON'T EVEN
            # OF COURSE THE FUCKING EVENT LOOP IS IN ANOTHER CLASS SOMEWHERE AND IT'S MASQUERADING AS A FUCKING
            # SPRITE PATH FOR A SPRITE TO FOLLOW BECAUSE I DON'T KNOW!
            
            # FUCK YOU IMAGINARY PERSON FOR JUDGING ME
            # MAYBE THERE IS A GOOD WAY TO DO IT BUT THE SAMPLES DO IT THIS WAY AND THE DOUMENTATION TALKS AS IF EVERYTHING SHOULD BE OBVIOUS
            # IT ISN'T
        )

        def _update(self, frame_no):
            super()._update(frame_no)


class AppLogic(DynamicRenderer):
    def __init__(self):
        super().__init__(1, 1)
        global selection
        self._enter_pressed= False
        self.menu_state = 3
        self._last_selection = selection
        self.menudelay = 0
        self._yes = False
        self._no = False
        #State 0 - Which Servo is Moving?
        #State 2 - Is the Servo at the Outer/Upper Movement? (Y/N)
        #State 3 - Logged! Thanks, Next Servo

    # I dunno how this fucking thing works but you can code here
    # It wasn't letting me do shit anywhere else so I made my own goddamn main loop
    def _render_now(self):
        # global timer
        global selection
        global current_menu_message

        if self._last_selection != selection:
            # current_menu_message[0]="Which Servo is Moving?; {}".format(selection)
            current_menu_message[0]="Which servo is moving? {} ".format(selection)

            self.menu_state = 1
        if self.menu_state == 1:
            self._last_selection = selection

            current_menu_message[1] ="Servo moved upper or outer extent (Y/N)?"
            if self._yes:
                current_menu_message[1] += "; Y"
                self.menu_state= 3
            if self._no:
                current_menu_message[1]+= "; N"
                self.menu_state = 3

        if self.menu_state == 3:
                current_menu_message= ["Moving a Sevo, Which Servo is moving?", " "," "]

        # currenttime = time.time()
        # if time.time()-timer > 1:
        #     if selection+1 < 5:
        #         selection += 1
        #         timer = time.time()
        #     else:
        #         selection = 1
        return self._plain_image, self._colour_map


    def enter_pressed(self):
        self._enter_pressed = True
    def yes(self):
        self._yes = True
        self._no = False
    def no(self):
        self._no = True 
        self._yes = False
    def selection_made(self, lselection):
        global selection
        if self.menu_state == 3:
            selection= lselection



class KeyboardController(DynamicPath):

    def process_event(self, event):
        global selection
        global current_menu_message
        keydict = {
            1: Screen.KEY_ADD
        }
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            print(key)
            if int(key) >=49 and int(key) <=56:
                logic.selection_made( int(key)-48 )

            elif key == 13:
                logic.enter_pressed()
            elif key == 110 or key == 121:
                if key == 121:
                    logic.yes()
                else:
                    logic.no()
            else:
                pass
        else:
            return event

logic = AppLogic()

def confugur(screen):
    global timer
    global selection
    global logic
    path = Path()
    path.jump_to(50, 12)
    effects = [NinjaRobotScroller(screen, path),
               Print(screen, SelectorBox(1), x=0, y=0),
               Print(screen, SelectorBox(3), x=18, y=0),
               Print(screen, SelectorBox(2), x=0, y=3),
               Print(screen, SelectorBox(4), x=18, y=3),
               Print(screen, SelectorBox(5), x=0, y=11),
               Print(screen, SelectorBox(7), x=18, y=11),
               Print(screen, SelectorBox(6), x=0, y=14),
               Print(screen, SelectorBox(8), x=18, y=14),
               Print(screen, NinjaMenu(), x=30, y=0),
               Print(screen, logic, 0, 0),
               KeyboardLogic(screen)]
    scenes = [Scene(effects, -1)]

    # # if time.time()-timer > 1:
    #     if selection+1 < 5:
    #         selection+=1
    #         timer = time.time()

    screen.play(scenes)

    # if time.time()-timer > 1:
    #     if selection+1 < 5:
    #         selection+=1
    #         timer = time.time()


Screen.wrapper(confugur)


# generate_scroller_frames()
