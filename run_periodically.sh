#!/bin/bash

if pgrep -x "python3" > /dev/null
then
    echo "Already running"
else
    python3 main.py
fi
