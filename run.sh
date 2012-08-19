#!/bin/sh
while true
do
python nemebot.py | tee logs/$(date "+%d-%m-%Y_%H:%M:%S").log
# update
done
