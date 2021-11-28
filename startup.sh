#!/bin/bash

# Startup script to activate development enviroment


# Activate virtual enviroment
source .venv/bin/activate


# Start database
mongod --config database/db.conf

# Status report
ls
git status
