#!/bin/sh
while true
do
git pull
python xmlnemebot.py | tee logs/$(date "+%d-%m-%Y_%H:%M:%S").log
done
