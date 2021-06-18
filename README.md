# AIO

Just like AIO-coolers, this little program aims to tackle many problems at once.


## What it mainly does
* chat-bot (via telegram)
* clock and basic display (via LED-Matrix (size to taste))
* dashboard (via external browser)


### Chatbot
Periodically calls the telegram api and reacts to sent commands. Also handles basic calls to the hardware: it allows you to control certain aspects of the clock.

TODO: advanced analytics of the chat (grafana)

## Clock
Server/Client which send/receive the output to show on the clock. Normally this is just a combination of time + weather. But special output can be triggered by the user.

## Dashboard
Shows basic info of the program and other useful things.

TODO: show advanced host stats (cpu/mem/...)
