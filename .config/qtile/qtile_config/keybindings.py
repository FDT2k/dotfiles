# keybindings.py - Key and mouse bindings


from libqtile.config import Key, Drag, Click
from libqtile.lazy import lazy

from .commands import mod, alt, ctrl, shft, command
from .workspaces import wsp, workspace_keys


def run_prompt(qtile):
    qtile.spawn(command.run)


def pick_theme(qtile):
    qtile.spawn(command.theme + ' ' + wsp['current'])


@lazy.function
def toggle_center(qtile):
    win = qtile.current_window
    if win:
        if win.floating:
            win.toggle_floating()  # repasse en tiling
        else:
            screen = qtile.current_screen
            sw = screen.width
            sh = screen.height
            w = int(sh * 16 / 9)
            x = (sw - w) // 2
            win.toggle_floating()
            win.set_size_floating(w, sh)
            win.set_position_floating(x, 0)

# Base keys
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
    Key([mod,shft], "f", toggle_center()),
    # Computer control
    Key([mod, ctrl], "r", lazy.restart()),
    Key([mod], "l", lazy.spawn(command.lock)),
    Key([mod], "Return", lazy.spawn(command.terminal)),

    Key([mod], "w", lazy.window.kill()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod], "Tab", lazy.screen.next_group()),
    Key([mod, shft], "Tab", lazy.screen.prev_group()),

    # app shortcuts
    #Key([mod, alt], "n", lazy.spawn("networkmanager_dmenu")),
    Key([mod, alt], "q", lazy.spawn(command.browser)),
    Key([mod, alt], "a", lazy.spawn(command.app_menu)),
    Key([mod], "r", lazy.function(run_prompt)),
    Key([mod, alt], "p", lazy.spawn(command.pacman)),
    Key([mod, ctrl], "p", lazy.spawn(command.power)),
    Key([mod], "b", lazy.spawn(command.bluetooth)),
    Key([mod], "n", lazy.spawn(command.network)),
    Key([mod, alt], "b", lazy.spawn(command.barrier)),
    Key([mod, alt], "t", lazy.function(pick_theme)),
    Key([mod, alt], "v", lazy.spawn(command.virt)),
    Key([mod], "p", lazy.spawn(command.worklayout)),

    Key([mod, alt], "e", lazy.spawn(command.configure)),
    Key([mod, alt], "s", lazy.spawn(command.sound)),
    Key([mod, alt], "l", lazy.spawn(command.screen_layout)),

    # screens options

    Key([mod, alt], "c", lazy.spawn(command.copyq)),

    Key([mod, alt], '9', lazy.spawn(command.volume_down)),

    # sounds & printscreen
    Key([], "XF86AudioLowerVolume", lazy.spawn(command.volume_down)),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(command.volume_up)),
    Key([], "XF86AudioMute", lazy.spawn(command.volume_mute)),
    Key([], 'Print', lazy.spawn(command.shoot)),
    Key([shft], 'Print', lazy.spawn(command.record)),
]

# ScratchPad keys
keys.extend([
    Key([mod, ctrl], "1", lazy.group['scratchpad'].dropdown_toggle('terminal')),
    Key([mod, ctrl], "2", lazy.group['scratchpad'].dropdown_toggle('Telegram')),
    Key([mod, ctrl], "4", lazy.group['scratchpad'].dropdown_toggle('discord')),
    Key([mod, ctrl], "5", lazy.group['scratchpad'].dropdown_toggle('blueman')),
    Key([mod, ctrl], "6", lazy.group['scratchpad'].dropdown_toggle('thunderbird')),
    Key([mod, ctrl], "8", lazy.group['scratchpad'].dropdown_toggle('gittyup')),
    Key([mod, ctrl], "9", lazy.group['scratchpad'].dropdown_toggle('mixer')),
    Key([mod, ctrl], "0", lazy.group['scratchpad'].dropdown_toggle('doc')),
])

# Workspace and room keybindings (from workspaces module)
keys.extend(workspace_keys)

# Mouse bindings
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Click([mod, shft], "Button1", lazy.window.toggle_floating()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]
