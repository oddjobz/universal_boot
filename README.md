# universal_boot

Update for for Universal Linux USB boot key

This code is still experimental - do not use.

For a pre-existing / formatted Universal boot key, this repository and associated code
are designed to allow the key to be updated on-the-fly with new or updated ISO images.

Boot a machine off the key, then run the init script to get going.

```bash
curl https://raw.githubusercontent.com/oddjobz/universal_boot/main/init.sh | bash
```

Currently the multiboot.py script does all the heavy lifting, just need to add
some sort of UI on the front (Zenity) to make it a little more usable.

```bash
usage: universal_boot.py [-h] [--list] [--update] [--add <iso>] [--verify <iso>] [--grub]

USB Key Maintenance

options:
  -h, --help      show this help message and exit
  --list          List available ISO's
  --update        Update software and signatures
  --add <iso>     The name of the ISO to add
  --verify <iso>  Verify the ISO's signatures
  --grub          Refresh the GRUB boot information

Free Software for Linux from Mad Penguin Consulting Ltd
```

Current ISO's we're sort of set up for (some of these need tweaking);

```bash
# ./universal_boot.py --list
ISO's Present on the USB Key:

ISO's Available for download:
> debian-12.11-cinnamon    |             | 3.10G | Debian (12.11) Cinnamon
> debian-12.11-gnome       |             | 3.20G | Debian (12.11) Gnome
> debian-12.11-kde         |             | 3.30G | Debian (12.11) KDE
> debian-13-kde            |             | 3.90G | Debian (Trixie) KDE
> debian-12.11-lxde        |             | 2.90G | Debian (12.11) LXDE
> debian-12.11-lxqt        |             | 3.00G | Debian (12.11) LXQT
> debian-12.11-mate        |             | 3.00G | Debian (12.11) MATE
> debian-12.11-standard    |             | 1.40G | Debian (12.11) Standard
> debian-12.11-xfce        |             | 3.00G | Debian (12.11) XFCE
> ubuntu-25.04             |             | 5.70G | Ubuntu (25.04) Gnome
> ubuntu-25.04-xfce        |             | 3.80G | Ubuntu (25.04) XFCE
> ubuntu-25.04-kde         |             | 4.70G | Ubuntu (25.04) KDE
> ubuntu-25.04-lxde        |             | 3.10G | Ubuntu (25.04) LXDE
> ubuntu-25.04-budgie      |             | 3.50G | Ubuntu (25.04) Budgie
> ubuntu-25.04-mate        |             | 3.90G | Ubuntu (25.04) MATE
> ubuntu-25.04-studio      |             | 4.70G | Ubuntu (25.04) Studio
> bodhi-7.0.0-standard     |             | 1.30G | Bodhi (7.0.0) Standard
> bodhi-7.0.0-hwe          |             | 1.30G | Bodhi (7.0.0) HWE
> rescue-12.0              |             | 0.86G | System Rescue (12.0)
> zorin-17.0               |             | 3.60G | Zorin Desktop (17.0)
> kali-2025.1c             |             | 4.60G | Kali Desktop (2025.1c) Live
> fedora-42-gnome          |             | 2.10G | Fedora (42) Gnome
> manjaro-25.0.6-gnome     |             | 3.90G | Manjaro (25.0.6) Gnome
> manjaro-25.0.6-kde       |             | 3.70G | Manjaro (25.0.6) KDE
> manjaro-25.0.6-xfce      |             | 3.60G | Manjaro (25.0.6) XFCE
> mint-22.1-cinnamon       |             | 2.90G | Mint (22.1) Cinnamon
> mint-22.1-mate           |             | 3.00G | Mint (22.1) Mate
> mint-22.1-xfce           |             | 2.90G | Mint (22.1) XFCE
> vanillaos-2025-02-20     |             | 1.92G | VanillaOS (2025-02)
> arch-2025.08.01          |             | 1.30G | Arch Linux (2025.08.01) Live
> sparky-7.8-lxqt          |             | 2.00G | Sparky (7.8) LXQt
> sparky-7.8-mate          |             | 2.20G | Sparky (7.7) Mate
> sparky-7.8-xfce          |             | 1.85G | Sparky (7.8) XFCE
> sparky-7.8-kde           |             | 2.30G | Sparky (7.8) KDE
> sparky-7.8-686-min       |             | 1.30G | Sparky (7.8) Min (32 bit)
> sparky-7.8-i686-cli      |             | 0.80G | Sparky (7.8) CLI (32 Bit)
```