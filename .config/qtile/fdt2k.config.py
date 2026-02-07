# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import sys
import os
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click, Match, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger
from typing import List  # noqa: F401

#from fdt2k_widgets import *

mod = "mod4"
alt = "mod1"
ctrl = "control"
shft = "shift"


# List of available workspaces.
# Each workspace has its own prefix and hotkey.
workspaces = [
    ('1', 'F1'),
    ('2', 'F2'),
    ('3', 'F3'),
    ('4', 'F4'),
    ('o', 'F5'),
    ('p', 'F6'),
]

# List of available rooms.
# Rooms are identical between workspaces, but they can
# be changed to different ones as well. Minor changes required.
rooms = "asdyxc"

# Oops, time for a little hack there.
# This is a global object with information about current workspace.
# (viable as config code, not sure about client-server though)
wsp = {
    'current': workspaces[0][0], # first workspace is active by default
}

@hook.subscribe.screen_change
def screen_change():
    qtile.cmd_restart()


@hook.subscribe.client_new
def agroup(client):
    # replace class_name with the actual
    # class name of the app
    # you can use xprop to find it
    apps = {
       
        'VirtualBox Manager': 'o',
        'Mail': 'p',
        'discord': 'p',
        'spotify': 'i',
        'Spotify': 'i',
        'crx_edcmabgkbicempmpgmniellhbjopafjh': 's',
        'calendar.google.com': 's',
        'bia-manager-electron':'d'
    }
    wm_class = client.window.get_wm_class()[0]
    group = apps.get(wm_class, None)
    logger.error("class %s %s" , wm_class,group)
    if group:
        client.togroup(get_group_name(wsp['current'], group))
        #to_room(group)
#        client.togroup(group)



home = os.path.expanduser('~')

# pywall import
# from https://github.com/gibranlp/QARSlp/blob/6da11eb970a8b2560912eddef1615ebbbc19a048/dotfiles/.config/qtile/funct.py#L26
##### Import Pywal Palette #####
with open(home + '/.cache/wal/colors.json') as wal_import:
    data = json.load(wal_import)
    wallpaper = data['wallpaper']
    alpha = data['alpha']
    colors = data['colors']
    val_colors = list(colors.values())

    def getList(val_colors):
        return [*val_colors]


def init_colors():
    return [*val_colors]


color = init_colors()


@lazy.function
def disable_mouse_focus():
    qtile.config.follow_mouse_focus = False
@lazy.function
def enable_mouse_focus():
    qtile.config.follow_mouse_focus = True




@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

class command:
    #terminal = get_alternatives(['terminator', 'gnome-terminal', 'xterm'])
    autostart = os.path.join(os.path.dirname(__file__), 'bin/autostart')
    lock = os.path.join(os.path.dirname(__file__), 'bin/lock')
    suspend = os.path.join(os.path.dirname(__file__), 'bin/suspend')
    hibernate = os.path.join(os.path.dirname(__file__), 'bin/hibernate')
    home_screen_layout = os.path.join(os.path.dirname(
        __file__), 'bin/monitor_layout/home-layout.sh')
    work_screen_layout = os.path.join(os.path.dirname(
        __file__), 'bin/monitor_layout/vertical_layout.sh')
    samsung_screen_layout = os.path.join(os.path.dirname(
        __file__), 'bin/monitor_layout/samsung-uwide-no-edp.sh')
    samsung_screen_dual_layout = os.path.join(os.path.dirname(
        __file__), 'bin/monitor_layout/samsung-uwide-with-edp.sh')
    terminal = "terminator -b"
    volume_up = os.path.join(os.path.dirname(__file__), 'bin/raisevolume')
    volume_down = os.path.join(os.path.dirname(__file__), 'bin/lowervolume')
    volume_mute = os.path.join(os.path.dirname(__file__), 'bin/mutevolume')
    shoot = os.path.join(os.path.dirname(__file__), 'bin/shot.sh')
    record = os.path.join(os.path.dirname(__file__), 'bin/record.sh')
    browser = os.path.join(os.path.dirname(__file__),
                           'bin/run.sh browser.d Browser')
    app_menu = os.path.join(os.path.dirname(__file__), 'bin/run.sh run.d App')
    configure = os.path.join(os.path.dirname(
        __file__), 'bin/run.sh configure.d Configure')
    #run = os.path.join(os.path.dirname(__file__), 'bin/run')
    run = os.path.join(os.path.dirname(__file__), 'bin/run')
    pacman = os.path.join(os.path.dirname(__file__),
                          'bin/run.sh pacman.d Pacman')
    barrier = os.path.join(os.path.dirname(__file__),
                           'bin/run.sh barrier.d Barrier')
    power = os.path.join(os.path.dirname(__file__),'bin/run.sh power.d Power')
    virt = os.path.join(os.path.dirname(__file__),'bin/run.sh osx.d Virt')
    worklayout = os.path.join(os.path.dirname(__file__),'bin/run.sh worklayout.d WorkLayout')
    #power = os.path.join(os.path.dirname(__file__),'rofi/powermenu.sh')
    middle_screen_brightness = os.path.join(
        os.path.dirname(__file__), 'bin/brightness.sh HDMI-A-1')
    right_screen_brightness = os.path.join(
        os.path.dirname(__file__), 'bin/brightness.sh DVI-I-1')
    left_screen_brightness = os.path.join(
        os.path.dirname(__file__), 'bin/brightness.sh HDMI-A-1-0')
    sound = os.path.join(os.path.dirname(__file__),
                         'bin/pulsaudio/sound-output.sh')
    theme = os.path.join(os.path.dirname(__file__), 'bin/theme/pick ' )
    screen_layout = os.path.join(os.path.dirname(
        __file__), 'bin/run.sh screenlayout.d "Monitor Layout"'),
    copyq = os.path.join(os.path.dirname(
        __file__), 'bin/copyq.sh'),


class theme:
    bg = color[0]
    fg = color[7]
    bg_active = color[1]
    contrasted = color[6]
    bg_other=  color[8]
     
    margin = 10

class theme_neg:
    bg = color[2]
    fg = color[0]
    bg_active = color[6]
    contrasted = color[7]
    bg_other=  color[6]
    
    margin = 10

def set_vertical_monitor_layout(qtile):
    qtile.cmd_spawn(command.home_screen_layout)

def run_prompt(qtile):
    qtile.cmd_spawn(command.run)

def set_horizontal_monitor_layout(qtile):
    qtile.cmd_spawn(command.work_screen_layout)


def set_samsung_monitor_layout(qtile):
    qtile.cmd_spawn(command.samsung_screen_layout)


def set_samsung_monitor_dual_layout(qtile):
    qtile.cmd_spawn(command.samsung_screen_dual_layout)


curr_screen = 0

def pick_theme(qtile):
     qtile.cmd_spawn(command.theme+' '+wsp['current'])

def toggle_screen_focus(qtile):
    global curr_screen
    screen_name = "middle"
    if curr_screen == 0:
        curr_screen = 1
        screen_name = "right"
    elif curr_screen == 1:
        curr_screen = 2
        screen_name = "left"
    else:
        curr_screen = 0

    qtile.cmd_spawn(
        "notify-send --hint=string:x-dunst-stack-tag:screenfocus  \"focused %s screen \"" % screen_name)
    qtile.cmd_to_screen(curr_screen)
    move_cursor(curr_screen)


def move_cursor(arg):
    screeninfo = [
        s for s in subprocess.check_output("xrandr").decode("utf-8").split()
        if s.count("+") == 2
    ]
   # logger.error("screens %s" , screeninfo)
    # if arg == "left":
    #    match = [s for s in screeninfo if s.endswith("+0+0")][0]
    # elif arg == "right":
    #    match = [s for s in screeninfo if not s.endswith("+0+0")][0]
    match = screeninfo[arg]
    data = [item.split("x") for item in match.split("+")]
   # logger.error("data %s" , data)

    numbers = [int(n) for n in [item for sublist in data for item in sublist]]
   # logger.error("numbers %s" , numbers)

    coord = [str(int(n))
             for n in [(numbers[0]/2)+numbers[2], (numbers[1]/2)+numbers[3]]]
   # logger.error("coords %s" , coord)

    subprocess.Popen(["xdotool", "mousemove", coord[0], coord[1]])


keys = [
    # Switch between windows in current stack pane
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod, shft], "space", lazy.layout.rotate()),



    # Move windows up or down in current stack
    Key([mod, ctrl], "Down", lazy.layout.shuffle_down()),
    Key([mod, ctrl], "Up", lazy.layout.shuffle_up()),
    Key([mod, ctrl], "Right", lazy.layout.shuffle_right()),
    Key([mod, ctrl], "Left", lazy.layout.shuffle_left()),

    Key([mod, alt], "Down", lazy.layout.grow_down()),
    Key([mod, alt], "Up", lazy.layout.grow_up()),
    Key([mod, alt], "Left", lazy.layout.grow_left()),
    Key([mod, alt], "Right", lazy.layout.grow_right()),


    Key([mod, alt, shft], "Down", lazy.layout.shrink()),
    Key([mod, alt, shft], "Up", lazy.layout.grow()),

    Key([mod, shft], "Return", lazy.layout.toggle_split()),

    Key([mod, shft], "n", lazy.layout.normalize()),

    # screen focus
    Key([mod], "q", lazy.function(toggle_screen_focus)),


    # Computer control
    Key([mod, ctrl], "r", lazy.restart()),
    #Key([mod, ctrl], "q", lazy.shutdown()),
    Key([mod], "l", lazy.spawn(command.lock)),
    Key([mod], "Return", lazy.spawn(command.terminal)),


    Key([mod], "w", lazy.window.kill()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod], "Tab", lazy.screen.next_group()),
    Key([mod, shft], "Tab", lazy.screen.prev_group()),
   # Key([mod, ctrl], "l", lazy.spawn(command.suspend)),




    # Toggle between different layouts as defined below


    #Key([mod], "r", lazy.spawncmd()),


    # app shortcuts

    Key([mod, alt], "n", lazy.spawn("networkmanager_dmenu")),
    Key([mod, alt], "q", lazy.spawn(command.browser)),
    Key([mod, alt], "a", lazy.spawn(command.app_menu)),
    #Key([mod], "r", lazy.spawn(command.run)),
    Key([mod], "r", lazy.function(run_prompt)),
    Key([mod, alt], "p", lazy.spawn(command.pacman)),
    Key([mod, ctrl], "p", lazy.spawn(command.power)),
    Key([mod, alt], "b", lazy.spawn(command.barrier)),
   # Key([mod, alt], "t", lazy.spawn(command.theme+' '+wsp['current'])),
    Key([mod, alt], "t", lazy.function(pick_theme)),
    Key([mod, alt], "v", lazy.spawn(command.virt)),
    Key([mod], "p", lazy.spawn(command.worklayout)),


    Key([mod, alt], "e", lazy.spawn(command.configure)),
    Key([mod, alt], "s", lazy.spawn(command.sound)),
    Key([mod, alt], "l", lazy.spawn(command.screen_layout)),

    # screens options
    Key([mod, alt], "2", lazy.spawn(command.middle_screen_brightness)),
    Key([mod, alt], "3", lazy.spawn(command.right_screen_brightness)),
    Key([mod, alt], "1", lazy.spawn(command.left_screen_brightness)),

    Key([mod, alt], "c", lazy.spawn(command.copyq)),
    

    # launch graphic layout
    #    Key([mod, alt], "y", lazy.function(set_vertical_monitor_layout)),
    #    Key([mod, alt], "x", lazy.function(set_horizontal_monitor_layout)),
    #    Key([mod, alt], "c", lazy.function(set_samsung_monitor_layout)),
    #    Key([mod, alt], "v", lazy.function(set_samsung_monitor_dual_layout)),

    Key([mod, alt], '9', lazy.spawn(command.volume_down)),


    # sounds & printscreen
    #Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(command.volume_down)),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(command.volume_up)),
    Key([], "XF86AudioMute", lazy.spawn(command.volume_mute)),
    # Key([mod,alt], "+", lazy.spawn(command.volume_up)),
    Key([], 'Print', lazy.spawn(command.shoot)),
    Key([shft], 'Print', lazy.spawn(command.record)),




]




# ----------------------------
# --- Workspaces and Rooms ---
# ----------------------------

# The basic idea behind Workspaces and Rooms is to control
# DIFFERENT subsets of groups with the SAME hotkeys.
# So we can have multiple 'qwerasdf' rooms in a different workspaces.
#
# Qtile Groups are used behind the scenes, but their visibility
# is set dynamically.

def get_group_name(workspace, room):
    """ Calculate Group name based on (workspace,room) combination.
    """
    return "%s%s" % (room, workspace)

# ... and information about active group in the each workspace.
for w, _ in workspaces:
    wsp[w] = {
        'active_group': get_group_name(w, rooms[0]) # first room is active by default
    }

def get_workspace_groups(workspace):
    """ Get list of Groups that belongs to workspace.
    """
    return [ get_group_name(workspace, room) for room in rooms]

def to_workspace(workspace):
    """ Change current workspace to another one.
    """

    def f(qtile):
        global wsp

        logger.error("showing workspace %s",workspace)
        # we need to save current active room(group) somewhere
        # to return to it later
        wsp[wsp['current']]['active_group'] = qtile.current_group.name

        # now we can change current workspace to the new one
        # (no actual switch there)
        wsp['current'] = workspace
        # and navigate to the active group from the workspace
        # (actual switch)
        #qtile.groups_map[
        #    wsp[workspace]['active_group']
        #].toscreen(toggle=False)
       
        #dispatch the workspace's groups in order on each screen
        for idx,screen in enumerate(qtile.screens):
            logger.error("changing screen %d",idx)

            g = qtile.groups_map[
                get_group_name(workspace,rooms[idx])
            ]
            logger.error("group %s",g)
            
            screen.set_group(g)
            logger.error("screen widgets %s",screen.top)
            if screen.top != None:
                for i,__widget in enumerate( screen.top.widgets):
                    logger.error("screens %s %s" , type(__widget) is widget.groupbox.GroupBox, __widget)
                    if type(__widget) is widget.groupbox.GroupBox :
                        __widget.visible_groups=get_workspace_groups(workspace)
                        __widget.draw()



        #set_group(self, new_group, save_prev=True, warp=True):
        # we also need to change subset of visible groups in the GroupBox widget
        #qtile.widgets_map['groupbox'].visible_groups=get_workspace_groups(workspace)

        #logger.error("screens %s" , qtile.widgets_map)
       # qtile.widgets_map['groupbox'].draw()
        # You can do some other cosmetic stuff here.
        # For example, change Bar background depending on the current workspace.
        #qtile.widgets_map['groupbox'].bar.background="ff0000"

        
    return f

def to_room(room):
    """ Change active room to another within the current workspace.
    """
    def f(qtile):
        global wsp
        qtile.groups_map[get_group_name(wsp['current'], room)].toscreen(toggle=False)
    return f

def window_to_workspace(workspace, room=rooms[0]):
    """ Move active window to another workspace.
    """
    def f(qtile):
        global wsp
        qtile.current_window.togroup(wsp[workspace]['active_group'])
    return f

def window_to_room(room):
    """ Move active window to another room within the current workspace.
    """
    def f(qtile):
        global wsp
        qtile.current_window.togroup(get_group_name(wsp['current'], room))
    return f

# Create individual Group for each (workspace,room) combination we have
groups = []
for workspace, hotkey in workspaces:
    for room in rooms:
        groups.append(Group(get_group_name(workspace, room)))

# Assign individual hotkeys for each workspace we have
for workspace, hotkey in workspaces:
    keys.append(Key([mod], hotkey, lazy.function(
        to_workspace(workspace))))
    keys.append(Key([mod, "shift"], hotkey, lazy.function(
        window_to_workspace(workspace))))


groups.append(ScratchPad(name='scratchpad', dropdowns=[
    DropDown('terminal', 'terminator', width=0.9,
             height=0.9, x=0.05, y=0.05, opacity=0.95, match =Match(wm_class='terminator'), on_focus_lost_hide=False),
    DropDown('spotify', 'spotify', width=0.8,
             height=0.8, x=0.1, y=0.1, opacity=0.8, match =Match(wm_class='spotify'), on_focus_lost_hide=False),
    DropDown('Telegram', 'org.telegram.desktop', width=0.8,
             height=0.8, x=0.1, y=0.1, opacity=1, match =Match(wm_class='TelegramDesktop'), on_focus_lost_hide=False),
    DropDown('mixer', 'pavucontrol', width=0.4,
             height=0.6, x=0.3, y=0.1, opacity=1),
    DropDown('bitwarden', 'bitwarden-desktop',
             width=0.6, height=0.6, x=0.2, y=0.1, opacity=1 ,match =Match(wm_class='bitwarden-desktop'), on_focus_lost_hide=False),
    DropDown('clickup', 'clickup',
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,match =Match(wm_class='clickup'), on_focus_lost_hide=False),
    DropDown('thunderbird', 'thunderbird',
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,on_focus_lost_hide=False),
    DropDown('blueman', 'blueman-manager',
             width=0.4, height=0.6, x=0.3, y=0.1, opacity=1 ,on_focus_lost_hide=False),
    DropDown('gittyup', 'gittyup',
              width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,match =Match(wm_class='gittyup'), on_focus_lost_hide=False),
    DropDown('doc', 'google-chrome-stable',
              width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,match =Match(wm_class='google-chrome'), on_focus_lost_hide=False),          
     DropDown('discord', 'com.discordapp.Discord',
              width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,match =Match(wm_class='discord'), on_focus_lost_hide=False),              
],single=True))

keys.extend([
    Key([mod,ctrl], "1", lazy.group['scratchpad'].dropdown_toggle('terminal')),
    Key([mod,ctrl], "2", lazy.group['scratchpad'].dropdown_toggle('Telegram')),
# Key([mod,ctrl], "3", lazy.group['scratchpad'].dropdown_toggle('bitwarden')),
    Key([mod,ctrl], "4", lazy.group['scratchpad'].dropdown_toggle('discord')),
    Key([mod,ctrl], "5", lazy.group['scratchpad'].dropdown_toggle('blueman')),
    Key([mod,ctrl], "6", lazy.group['scratchpad'].dropdown_toggle('thunderbird')),
    Key([mod,ctrl], "8", lazy.group['scratchpad'].dropdown_toggle('gittyup')),
    Key([mod,ctrl], "9", lazy.group['scratchpad'].dropdown_toggle('mixer')),
    Key([mod,ctrl], "0", lazy.group['scratchpad'].dropdown_toggle('doc')),
 #   Key([mod,ctrl], "d", lazy.group['scratchpad'].dropdown_toggle('discord')),

])

# Assign shared hotkeys for each room we have.
# Decision about actual group to open is made dynamically.
for room in rooms:
    keys.append(Key([mod], room, lazy.function(
        to_room(room))))
    keys.append(Key([mod, "shift"], room, lazy.function(
        window_to_room(room))))

#end of workspaces

layouts = [
    #    layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    layout.Max(
          border_width=2,
        border_focus=theme.bg_active,
        border_normal=theme.bg,
        margin=theme.margin
    ),
    layout.Bsp(
        border_width=4,
        border_focus=theme.bg_active,
        border_normal=theme.bg,
        margin=theme.margin
    ),
    #     layout.Columns(),
    # layout.Matrix(),
    #layout.MonadTall(),
    #layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    layout.TreeTab(
      
       # active_fg=theme.bg_active,
        active_bg=theme.bg_active,
        bg_color=theme.bg,
        panel_width=200,
          border_width=2,
        border_focus=theme.bg_active,
        border_normal=theme.bg,
        margin=theme.margin,
        section_top=theme.margin,
        section_bottom=theme.margin,
        margin_left=theme.margin,
        margin_y = theme.margin,
        padding_y = theme.margin
    ),
    # layout.VerticalTile(),
    #layout.Zoomy(columnwidth=500),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

FONT_SIZE = 12

"""
               
                widget.TextBox(
                    font="Arial",
                    foreground=color[0],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[1],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[2],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[3],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[4],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[5],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[6],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[7],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                 widget.TextBox(
                    font="Arial",
                    foreground=color[8],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),

                 widget.TextBox(
                    font="Arial",
                    foreground=color[9],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                 widget.TextBox(
                    font="Arial",
                    foreground=color[10],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                 widget.TextBox(
                    font="Arial",
                    foreground=color[11],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                """

screens = [
    Screen(
        top=bar.Bar(
           
            [
                widget.Spacer(10),
            
                widget.CurrentLayout(),
               
                widget.TextBox(
                    font="Arial",
                    foreground=theme_neg.bg,
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.GroupBox(disable_drag=True,
                                background=theme_neg.bg,
                                foreground=theme_neg.fg,
                                active=theme_neg.fg,
                                inactive=theme_neg.contrasted,
                                this_current_screen_border=theme.bg,
                                other_current_screen_border=theme.bg_other,
                                other_screen_border=theme.bg_other,
                                borderwidth=1,
                                highlight_method='border',
                                font='Open Sans',
                                fontsize=12,
                                visible_groups=get_workspace_groups(wsp['current']),
                                ),
                widget.TextBox(
                    font="Arial",
                    foreground=theme_neg.bg,
                    text="◤ ",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.Prompt(),


                widget.WindowName(padding=0),

                # widget.TextBox("default config", name="default"),

                widget.TextBox(
                    font="Arial",
                    foreground="#CACACA",
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.NetGraph(
                    bandwidth_type="up",
                    type="linefill",
                    background="#CACACA",

                    line_width=1
                ),

                widget.CPUGraph(
                    type="box",
                    graph_color=theme.bg_active,
                    border_color=theme.bg_active,
                    background="#CACACA",
                    border_width=2,
                    line_width=1
                ),
                widget.MemoryGraph(
                    type="box",
                    graph_color=theme.bg_active,
                    border_color=theme.bg_active,
                    background="#CACACA",

                    border_width=2,
                    line_width=1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground="#CACACA",
                    text="◤ ",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.Systray(),
                widget.Clock(format='%d.%m.%Y %H:%M'),

                #       widget.Volume(get_volume_command="pamixer --get-volume",emoji=True),
                widget.QuickExit(),
                widget.Spacer(10),
            ],
            28,
            background=theme.bg,
            margin= [10,10,0,10],
            

        ),
    ),
     Screen(),
    #Screen(
    #    top=bar.Bar([
    #        widget.Spacer(10),
    #            widget.CurrentLayout(),
    #           
    #            widget.TextBox(
    #                font="Arial",
    #                foreground=theme_neg.bg,
    #                text="◢",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #            widget.GroupBox(disable_drag=True,
    #                            background=theme_neg.bg,
    #                            foreground=theme_neg.fg,
    #                            active=theme_neg.fg,
    #                            inactive=theme_neg.contrasted,
    #                            this_current_screen_border=theme.bg,
    #                            other_current_screen_border=theme.bg_other,
    #                            other_screen_border=theme.bg_other,
    #                            borderwidth=1,
    #                            highlight_method='border',
    #                            font='Open Sans',
    #                            fontsize=12,
    #                            visible_groups=get_workspace_groups(wsp['current']),
    #                            ),
    #            widget.TextBox(
    #                font="Arial",
    #                foreground=theme_neg.bg,
    #                text="◤ ",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #            widget.Prompt(),
#
#
    #            widget.WindowName(padding=0),
#
    #            # widget.TextBox("default config", name="default"),
#
    #            widget.TextBox(
    #                font="Arial",
    #                foreground="#CACACA",
    #                text="◢",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #            widget.NetGraph(
    #                bandwidth_type="up",
    #                type="linefill",
    #                background="#CACACA",
#
    #                line_width=1
    #            ),
#
    #            widget.CPUGraph(
    #                type="box",
    #                graph_color=theme.bg_active,
    #                border_color=theme.bg_active,
    #                background="#CACACA",
    #                border_width=2,
    #                line_width=1
    #            ),
    #            widget.MemoryGraph(
    #                type="box",
    #                graph_color=theme.bg_active,
    #                border_color=theme.bg_active,
    #                background="#CACACA",
#
    #                border_width=2,
    #                line_width=1
    #            ),
    #            widget.TextBox(
    #                font="Arial",
    #                foreground="#CACACA",
    #                text="◤ ",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #          widget.Spacer(10),
    #           
    #        ], 28,background=theme.bg, margin= [10,10,0,10]),
    #),
    #Screen(
    #    top=bar.Bar([
    #        widget.Spacer(10),
    #            widget.CurrentLayout(),
    #           
    #            widget.TextBox(
    #                font="Arial",
    #                foreground=theme_neg.bg,
    #                text="◢",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #           widget.GroupBox(disable_drag=True,
    #                            background=theme_neg.bg,
    #                            foreground=theme_neg.fg,
    #                            active=theme_neg.fg,
    #                            inactive=theme_neg.contrasted,
    #                            this_current_screen_border=theme.bg,
    #                            other_current_screen_border=theme.bg_other,
    #                            other_screen_border=theme.bg_other,
    #                            borderwidth=1,
    #                            highlight_method='border',
    #                            font='Open Sans',
    #                            fontsize=12,
    #                            visible_groups=get_workspace_groups(wsp['current']),
    #                            ),
    #            widget.TextBox(
    #                font="Arial",
    #                foreground=theme_neg.bg,
    #                text="◤ ",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #            widget.Prompt(),
#
#
    #            widget.WindowName(padding=0),
#
    #            # widget.TextBox("default config", name="default"),
#
    #            widget.TextBox(
    #                font="Arial",
    #                foreground="#CACACA",
    #                text="◢",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #            widget.NetGraph(
    #                bandwidth_type="up",
    #                type="linefill",
    #                background="#CACACA",
#
    #                line_width=1
    #            ),
#
    #            widget.CPUGraph(
    #                type="box",
    #                graph_color=theme.bg_active,
    #                border_color=theme.bg_active,
    #                background="#CACACA",
    #                border_width=2,
    #                line_width=1
    #            ),
    #            widget.MemoryGraph(
    #                type="box",
    #                graph_color=theme.bg_active,
    #                border_color=theme.bg_active,
    #                background="#CACACA",
#
    #                border_width=2,
    #                line_width=1
    #            ),
    #            widget.TextBox(
    #                font="Arial",
    #                foreground="#CACACA",
    #                text="◤ ",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #             widget.Systray(),
    #          widget.Spacer(10),
    #           
    #        ], 28,background=theme.bg, margin= [10,10,0,10]),
    #)
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Click([mod, shft], "Button1", lazy.window.toggle_floating()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
""" floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'copyq'},
    {'role': 'dialog'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'xcalc'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {'wmclass': 'eww'}
], border_color=theme.bg_active) """

floating_layout = layout.Floating(float_rules=[
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='copyq'),
    Match(wm_class="xcalc"),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='bitwarden'),
    Match(wm_class='blueman-manager'),
    Match(func=lambda c: c.has_fixed_size()),
    Match(func=lambda c: c.has_fixed_ratio())
], border_normal=theme.fg, border_focus=theme.bg,border_width=4)

auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

