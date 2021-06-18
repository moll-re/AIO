## What is happening here?

This "persistence"-module aims to standardize 2 things:
* the creation of a common set of variables that survives a potential (let's face it, likely) crash
* advanced logging and analytics

### Common variables
These are saved as a json file and are handled internally as a dict. Each change in the dict triggers a write to the file.


### Logging
A chunky sqlite-db which periodically gets new entries. From all modules. Ideally this db is then visualized through grafana. WIP