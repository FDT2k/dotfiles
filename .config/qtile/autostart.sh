#!/bin/bash

DIR=$(dirname $0)
$DIR/bin/theme/reload &

#telegram-desktop &
#thunderbird &
#bin/clickup &
xss-lock -- $DIR/bin/i3lock-multimonitor/lock &

notify-send "autostart"

#tmux new -d -s ndb -c ~/Documents/work/fuge_workspaces "fuge shell microservice_dev/dev.yml"

sleep 1
killall -9 aw-qt
killall -9 aw-server
killall -9 aw-watcher-afk
killall -9 aw-watcher-window

killall -9 picom



aw-qt &
#xiccd & 
copyq &

#colormgr device-add-profile "xrandr-Samsung Electric Company-S34J55x-H4ZMC01890" icc-baa5c26a2b05f1d90d199da25b68342c
#colormgr device-make-profile-default "xrandr-Samsung Electric Company-S34J55x-H4ZMC01890" icc-baa5c26a2b05f1d90d199da25b68342c
#colormgr device-add-profile "xrandr-Ancor Communications Inc-ASUS VS238-BCLMTF008344" icc-25c894e53bcc148a0c87e9f6b8fc5ebc
#colormgr device-make-profile-default "xrandr-Ancor Communications Inc-ASUS VS238-BCLMTF008344" icc-25c894e53bcc148a0c87e9f6b8fc5ebc
#colormgr device-add-profile "xrandr-Philips Consumer Electronics Company-PHL 243V5-ZV0154600052" icc-838906326b91713ba34c223e832a68f8
#colormgr device-make-profile-default "xrandr-Philips Consumer Electronics Company-PHL 243V5-ZV0154600052" icc-838906326b91713ba34c223e832a68f8



#colormgr device-set-enabled "xrandr-Ancor Communications Inc-ASUS VS238-BCLMTF008344" True
#colormgr device-set-enabled "xrandr-Philips Consumer Electronics Company-PHL 243V5-ZV0154600052" True
#colormgr device-set-enabled "xrandr-Samsung Electric Company-S34J55x-H4ZMC01890" True
#colormgr device-set-enabled "xrandr-Samsung Electric Company-LS49A950U-HNTW500196" True
#colormgr device-set-enabled "xrandr-Invalid Vendor Codename - RTK-Verbatim MT1-demoset-1" True
#compton &


#picom --config ~/.config/qtile/.conf/picom.conf &


##feh --bg-fill ~/background.jpg &
#xinput --map-to-output 14 DisplayPort-4
#xinput --map-to-output 12 DisplayPort-5
#xinput --map-to-output 13 DisplayPort-6

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



#dispwin -d 3 -I ~/.local/share/color/icc/verbatim_dp5_centre.icc
#dispwin -d 2 -I ~/.local/share/color/icc/verbatim_dp4.icc

