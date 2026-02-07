#!/bin/zsh
screen=$1
value=$(echo "" | rofi -dmenu -p "Enter brightness  (1-10) > "  -theme-str 'listview { enabled: false;}' ); 
xrandr --output $screen --brightness $(($value.0/10))