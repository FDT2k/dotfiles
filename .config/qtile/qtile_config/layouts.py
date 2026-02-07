# layouts.py - Layout definitions

from libqtile import layout

from .themes import theme

layouts = [
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
    layout.TreeTab(
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
        margin_y=theme.margin,
        padding_y=theme.margin
    ),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

FONT_SIZE = 12
