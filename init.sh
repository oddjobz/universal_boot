#!/usr/bin/env bash
MNT=/run/live/findiso
DST=${MNT}/universal_boot
sudo apt update
sudo apt install -y python3-pip git libcurl4-openssl-dev libssl-dev whiptail rainbow-tqdm
sudo pip install pgpy jinja2 tqdm pycurl rainbow_tqdm whiptail-dialogs psutil whiptail --break-system-packages
sudo mount -o remount,rw ${MNT}
sudo git -C ${DST} config --global --add safe.directory ${DST}
sudo git -C ${DST} pull
echo "Universal Loader Ready>"
cd ${DST} && sudo ./universal_boot.py --update
cd ${DST} && sudo ./universal_boot.py --gui
cd ${DST} && exec bash