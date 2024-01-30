#!/usr/bin/env bash
apt install -y python3-pip git
pip install pgpy jinja2 tqdm --break-system-packages
mount -o remount,rw /run/live/findiso
cd /run/live/findiso
https://github.com/oddjobz/universal_boot.git
