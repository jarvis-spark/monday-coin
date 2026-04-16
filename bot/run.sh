#!/bin/bash
cd "$(dirname "$0")"
source .env 2>/dev/null || true
pip install -r requirements.txt -q
python bot.py
