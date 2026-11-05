#!/bin/bash

DIR=$(dirname $0)
# Default screen layout of this machine, before the wallpaper is set
$DIR/bin/screenlayout --default
$DIR/bin/theme/reload &

xss-lock -- $DIR/bin/i3lock-multimonitor/lock &

notify-send "autostart"

sleep 1
killall -9 aw-qt
killall -9 aw-server
killall -9 aw-watcher-afk
killall -9 aw-watcher-window

killall -9 picom

aw-qt &
copyq &

map_touch() {
    local by_path="$1"
    local output="$2"
    local node=$(readlink -f "/dev/input/by-path/$by_path")
    local id=""
    for i in $(xinput list | grep -oP 'SiS HID Touch Controller\s+id=\K[0-9]+'); do
        if xinput list-props "$i" 2>/dev/null | grep -q "$node"; then
            id="$i"
            break
        fi
    done
    [ -n "$id" ] && xinput --map-to-output "$id" "$output"
}

map_touch "pci-0000:0d:00.3-usb-0:3.1.4.1:1.0-event" DisplayPort-5
map_touch "pci-0000:0d:00.3-usb-0:3.2.2.3:1.0-event" DisplayPort-4
map_touch "pci-0000:0d:00.3-usb-0:3.2.1.1:1.0-event" DisplayPort-6

