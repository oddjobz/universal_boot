#!/usr/bin/env bash
export MNT=/run/live/findiso
export DST=${MNT}/universal_boot
export PATH=$PATH:/root/.local/bin
apt update
apt -y install git python3-pip git libcurl4-openssl-dev libssl-dev whiptail pipx
pipx install poetry
git -C ${DST} config --global --add safe.directory ${DST}
git -C ${DST} pull
cd ${DST}
mount -o remount,rw ${MNT}
poetry env use python3
poetry install
poetry run ./universal_boot.py --update
poetry run ./universal_boot.py --gui
echo "Universal Loader Ready>"