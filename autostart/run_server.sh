#!/bin/bash

sleep 15 # gpio not inited right after boot?

cd /home/pi/AIO/
VE/bin/python3 server.py
