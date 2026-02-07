#!/bin/sh

DIR=$(dirname $0)
SCR=$(basename $0)


#force refreshing plugged monitors
xrandr
xrandr --output eDP-1 --primary --mode 1920x1080 --pos 0x1080 --rotate normal --output HDMI-1 --mode 1920x1080 --pos 0x0 --rotate normal


pushd $DIR/..

rm -f last-layout
ln -s monitor_layout/$SCR last-layout
#popd
