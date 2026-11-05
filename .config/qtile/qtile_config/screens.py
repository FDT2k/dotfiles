# screens.py - Screen and bar configurations

import os

from libqtile.config import Screen
from libqtile import bar, widget

from .themes import theme, theme_neg, wallpaper
from .layouts import FONT_SIZE
from .workspaces import wsp, get_workspace_groups

# Wallpaper: hellwal does not set it (pywal's `wal -i` did), so Qtile does,
# from the image recorded in colors.json. Missing image: no wallpaper.
if wallpaper and os.path.isfile(wallpaper):
    wallpaper_args = {'wallpaper': wallpaper, 'wallpaper_mode': 'fill'}
else:
    wallpaper_args = {}

screens = [

    Screen(
        top=bar.Bar(
            [
                widget.Spacer(10),
                widget.CurrentLayout(),
                widget.TextBox(
                    font="Arimo",
                    foreground=theme_neg.bg,
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.GroupBox(
                    disable_drag=True,
                    background=theme_neg.bg,
                    foreground=theme_neg.fg,
                    active=theme_neg.fg,
                    inactive=theme_neg.inactive,
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
                    font="Arimo",
                    foreground=theme_neg.bg,
                    text="◤ ",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.Prompt(),
                widget.WindowName(padding=0),
                widget.TextBox(
                    font="Arimo",
                    foreground=theme_neg.bg,
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.NetGraph(
                    bandwidth_type="up",
                    type="linefill",
                    graph_color=theme_neg.fg,
                    border_color=theme_neg.fg,
                    background=theme_neg.bg,
                    line_width=1
                ),
                widget.CPUGraph(
                    type="box",
                    graph_color=theme_neg.fg,
                    border_color=theme_neg.fg,
                    background=theme_neg.bg,
                    border_width=2,
                    line_width=1
                ),
                widget.MemoryGraph(
                    type="box",
                    graph_color=theme_neg.fg,
                    border_color=theme_neg.fg,
                    background=theme_neg.bg,
                    border_width=2,
                    line_width=1
                ),
                widget.TextBox(
                    font="Arimo",
                    foreground=theme_neg.bg,
                    text="◤ ",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.Systray(),
                widget.Clock(format='%d.%m.%Y %H:%M'),
                widget.QuickExit(),
                widget.Spacer(10),
            ],
            28,
            background=theme.bg,
            margin=[10, 10, 0, 10],
        ),
        **wallpaper_args,
    ),
    Screen(**wallpaper_args),

    Screen(**wallpaper_args),
    Screen(**wallpaper_args),
]
