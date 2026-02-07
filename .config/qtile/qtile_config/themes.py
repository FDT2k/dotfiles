# themes.py - Pywal color integration and theme classes

import json
import os

home = os.path.expanduser('~')

# Pywal import
# from https://github.com/gibranlp/QARSlp/blob/6da11eb970a8b2560912eddef1615ebbbc19a048/dotfiles/.config/qtile/funct.py#L26
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


class theme:
    bg = color[0]
    fg = color[7]
    bg_active = color[1]
    contrasted = color[6]
    bg_other = color[8]
    margin = 10


class theme_neg:
    bg = color[2]
    fg = color[0]
    bg_active = color[6]
    contrasted = color[7]
    bg_other = color[6]
    margin = 10
