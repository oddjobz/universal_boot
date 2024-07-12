#!/usr/bin/env bash
sudo apt install -y python3-pip git libcurl4-openssl-dev libssl-dev whiptail
sudo pip install pgpy jinja2 tqdm pycurl rainbow_tqdm whiptail-dialogs psutil whiptail rainbow_tqdm --break-system-packages
sudo mount -o remount,rw ${MNT}
echo "Universal Loader Ready>"
cd ${DST} && sudo ./universal_boot.py --update
cd ${DST} && sudo ./universal_boot.py --gui
cd ${DST} && exec bash