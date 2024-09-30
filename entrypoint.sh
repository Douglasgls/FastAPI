#!/bin/bash

alembic upgrade head

fastapi dev fast_zero/app.py --host 0.0.0.0 --port 7000