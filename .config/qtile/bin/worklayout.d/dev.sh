#!/bin/bash
qtile cmd-obj -o cmd -f eval -a "qtile.disable_mouse_focus()"

qtile cmd-obj -o group -f setlayout -a bsp

# Lancer vscode et l'agrandir
code &
sleep 1


# Lancer terminator
terminator &
sleep 2
qtile cmd-obj -o layout -f left
qtile cmd-obj -o layout -f grow_right
qtile cmd-obj -o layout -f grow_right
qtile cmd-obj -o cmd -f eval -a "qtile.enable_mouse_focus()"