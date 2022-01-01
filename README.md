# AIO

Just like AIO-coolers, this little program aims to tackle many problems at once.


## What it mainly does
* chat-bot (via telegram)
* clock and basic display (via LED-Matrix (size to taste))
* measure ambient temperatures
* Logging of the previous actions


### Chatbot
Periodically calls the telegram api and reacts to sent commands. Also handles basic calls to the hardware: it allows you to control certain aspects of the clock.


### Clock
Server/Client which send/receive the output to show on the clock. Normally this is just a combination of time + weather. But special output can be triggered by the user.

### Ambient measurements
Logs temperature, luminosity, humidity to a remote database. This information is then displayed in `moll.re`.

TODO: Log relevant worker info such as cpu activity and network connectivity.


## Submodules
This program makes use of git submodules, namely `sql_as_rest_api`. This implies additional steps when cloning this repo:

* CLone **this** repo to your machine.
* Enter the repo
* Type `git submodule init` which creates a `.gitmodules` file
* Type `git submodule update` which fetches the newest version of these submodules

TODO Describe dev process