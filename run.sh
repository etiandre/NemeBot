#!/bin/sh
while true
do
git pull
python nemebot.py | tee logs/$(date "+%d-%m-%Y_%H:%M:%S").log
done
