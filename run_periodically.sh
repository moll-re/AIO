#!/bin/bash

if pgrep -x "python3" > /dev/null
then
    python3 main.py
else
    echo "Not running"
fi
