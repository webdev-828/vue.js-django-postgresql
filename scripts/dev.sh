#!/bin/bash

# pg_ctl -D tmp/postgres -l logfile start

source ./.venv/bin/activate
honcho -f Procfile.dev start
