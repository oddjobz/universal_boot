#!/usr/bin/env bash
apt install python3-pip git
pip install pgpy jinja2 tqdm --break-system-packages
mount -o remount,rw /run/live/findiso
