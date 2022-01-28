#!/bin/bash

# Startup script to activate development enviroment


# Activate virtual enviroment
source .venv/397/bin/activate


# Start database
mongod --fork --config database/db.conf

# Status report
ls
git status
