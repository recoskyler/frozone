#!/bin/bash

# Usage: frozone.sh "command" X-OFFSET Y-OFFSET WIDTH HEIGHT DESKTOP

export DISPLAY=$DISPLAY

$1 & # start app

cpid=$! # get process ID of said app

sleep 1 # give it a second to open the window (adjust to needs)

cwid=$(wmctrl -lp | grep " $cpid " | cut -d " " -f 1) # get window ID

wmctrl -s $6 # switch to desktop
xdotool set_desktop $6 # switch to desktop
wmctrl -i -r "$cwid" -e "0,$2,$3,$4,$5" # move and resize!
wmctrl -i -r "$cwid" -b "remove,maximized_vert,maximized_horz" # un-maximize
wmctrl -i -r "$cwid" -t $6 # move to desktop 1 (2nd workspace)
