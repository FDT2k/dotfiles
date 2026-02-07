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
xiccd & 
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
colormgr device-set-enabled "xrandr-Samsung Electric Company-LS49A950U-HNTW500196" True
colormgr device-set-enabled "xrandr-Invalid Vendor Codename - RTK-Verbatim MT1-demoset-1" True
#compton &


#picom --config ~/.config/qtile/.conf/picom.conf &


#feh --bg-fill ~/background.jpg &
