# hooks.py - Qtile hook subscriptions

import os
import subprocess

from libqtile import hook
from libqtile.lazy import lazy
from libqtile.log_utils import logger

from .workspaces import wsp, get_group_name


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
        'bia-manager-electron': 'd'
    }
    wm_class = client.window.get_wm_class()[0]
    group = apps.get(wm_class, None)
    logger.error("class %s %s", wm_class, group)
    if group:
        client.togroup(get_group_name(wsp['current'], group))


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


@lazy.function
def disable_mouse_focus(qtile):
    qtile.config.follow_mouse_focus = False


@lazy.function
def enable_mouse_focus(qtile):
    qtile.config.follow_mouse_focus = True
