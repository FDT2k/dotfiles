#!/bin/bash

DIR=$(dirname $0)

OPTS=$(pactl list short sinks)

STR="$2"

declare -A sinks

OIFS=$IFS
IFS=$'\r\n'
for s in $OPTS 
do
    IDX=$(echo $s | awk '{print $1}')
    LABEL=$(echo $s | awk '{print $2}')
    sinks[$IDX]=$LABEL
done

IFS=$OIFS



function getTextOptions {
    sep=""
    for item in ${sinks[*]}; 
    do 
        default=""
        [[ "${item}" == "$(getDefaultSink)" ]] && default="*";

        options="${options}${sep}${default}${item}" ;
        sep="\n"
    done;
    echo "$options"
}

function getDefaultSink {
   echo $(pacmd info |grep "Default sink" | sed -E 's/^\s*[^:]*:(.*)$/\1/gm;t;d')
}



function getArrayIndex  {
    for key in ${!sinks[*]} 
    do 
        [[ ${sinks[$key]} == $choice ]] && index=$key
    done;
    echo $index
}


function moveSinks {
    TARGET=$1
    pactl list short sink-inputs|while read stream; do
        streamId=$(echo $stream|cut '-d ' -f1)
        echo "moving stream $streamId"
        pactl move-sink-input "$streamId" "$(getArrayIndex)"
    done
}


choice=$(echo -e "$(getTextOptions)" | rofi -lines 5 -dmenu -p "Sound Output")

moveSinks $(getArrayIndex)

pactl set-default-sink $(getArrayIndex)
#PATH=$PATH:$DIR bash $DIR/$1/$choice

