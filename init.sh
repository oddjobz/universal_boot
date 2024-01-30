#!/usr/bin/env bash
apt install -y python3-pip git
pip install pgpy jinja2 tqdm --break-system-packages
mount -o remount,rw /run/live/findiso
cd /run/live/findiso
sudo git config --global --add safe.directory /run/live/findiso/universal_boot
sudo git update
