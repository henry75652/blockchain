#!/bin/sh

#開滑鼠腳本

cd /home/pi/'Mission Planner'/logs/QUADROTOR/1

ls > name.txt

loopTime=0

while read line ; do
    loopTime=`expr $loopTime + 1`
done < name.txt

loopTime_txt=0
while read line ; do
    loopTime=`expr $loopTime + 1`
    if $loopTime_txt == $loopTime; then
    $txt = $line
fi
done

mavlogdump.py $txt > '1.txt'
