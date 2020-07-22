#!/bin/bash

if pgrep -x "python3" > /dev/null
then
    echo "Already running"
else
    cd /root/chat-bot/
    python3 main.py
fi
