#!/bin/sh
# Also run by SDDM before the login screen, through the link screenlayout.d/sddm
# and /etc/sddm.conf.d/10-dotfiles.conf (install-arch-deps.sh sddm): do not
# rename the sddm link.
xrandr --output DisplayPort-4 --mode 1920x1080 --pos 698x1440 --rotate normal --output DisplayPort-5 --off --output DisplayPort-6 --mode 1920x1080 --pos 2618x1440 --rotate normal --output DisplayPort-7 --primary --mode 5120x1440 --pos 0x0 --rotate normal --output DisplayPort-1-0 --off --output DisplayPort-1-1 --off --output DisplayPort-1-2 --off --output DisplayPort-1-3 --off
