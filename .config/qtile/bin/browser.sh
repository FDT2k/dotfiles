#!/bin/bash
#  ____ _____

declare options=("brave
chrome
chromium
firefox
quit")

choice=$(echo -e "${options[@]}" | cldmenu -i -p 'Browser: ')

case "$choice" in
	quit)
		echo "Program terminated." && exit 1
	;;
	brave)
		choice="brave"
	;;
	chrome)
		choice="google-chrome-stable"
	;;
	chromium)
		choice="chromium"
	;;
	firefox)
		choice="firefox"
	;;
	*)
		exit 1
	;;
esac
$choice &
