# screens.py - Screen and bar configurations

from libqtile.config import Screen
from libqtile import bar, widget

from .themes import theme, theme_neg
from .layouts import FONT_SIZE
from .workspaces import wsp, get_workspace_groups

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
                widget.GroupBox(
                    disable_drag=True,
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
                widget.QuickExit(),
                widget.Spacer(10),
            ],
            28,
            background=theme.bg,
            margin=[10, 10, 0, 10],
        ),
    ),
    Screen(),
]
