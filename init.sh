#!/usr/bin/env bash
MNT=/run/live/findiso
DST=${MNT}/universal_boot
sudo apt install -y python3-pip git
sudo pip install pgpy jinja2 tqdm --break-system-packages
sudo mount -o remount,rw ${MNT}
sudo git -C ${DST} config --global --add safe.directory ${DST}
sudo git -C ${DST} pull
echo "Universal Loader Ready>"

