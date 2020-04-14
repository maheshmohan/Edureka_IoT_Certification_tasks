#!/bin/sh

cd /home/pi/edureka_iot_works/M5/casestudy
python3 app.py&
xdg-open "http://127.0.0.1:5000/"
