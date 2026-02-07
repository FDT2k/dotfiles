# Qtile Configuration Package
# Main entry point - exports all Qtile configuration variables

from libqtile.config import Match
from libqtile import layout
from typing import List  # noqa: F401

# Import all modules to ensure hooks are registered
from .themes import color, theme, theme_neg
from .commands import mod, alt, ctrl, shft, command
from .workspaces import workspaces, rooms, wsp, groups, get_group_name, get_workspace_groups
from .layouts import layouts, widget_defaults, extension_defaults, FONT_SIZE
from .keybindings import keys, mouse
from .screens import screens
from . import hooks  # Import to register hook decorators

# Qtile configuration variables
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

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
], border_normal=theme.fg, border_focus=theme.bg, border_width=4)

auto_fullscreen = True
focus_on_window_activation = "smart"

# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
