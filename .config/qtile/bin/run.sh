#!/bin/zsh
#  ____ _____

DIR=$(dirname $0)

OPTS=$(ls -1 $DIR/$1)

STR="$2"



#IFS=$'\r\n' GLOBIGNORE='*' command eval  'COUNTS=($(cat $DIR/$1/.counts))'

#echo $COUNTS;
echo $STR
    
#choice=$(echo -e "$OPTS" | cldmenu -b  -i -p "$STR")
choice=$(echo -e "$OPTS" | rofi -lines 5 -dmenu -p "$STR")


PATH=$PATH:$DIR bash $DIR/$1/$choice
