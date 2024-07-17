#!/usr/bin/env bash
MNT=/run/live/findiso
DST=${MNT}/universal_boot
sudo apt update
sudo apt -y install git
sudo git -C ${DST} config --global --add safe.directory ${DST}
sudo git -C ${DST} pull
source ${DST}/init_2.sh
