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
usage: multiboot.py [-h] [--list] [--update] [--add <iso>] [--verify <iso>] [--grub]

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
$ ./multiboot.py --list
ISO's Present on the USB Key:

ISO's Available for download:
> debian-12.1                      => Debian Desktop - 12.1  - Gnome
> ubuntu-23.04                     => Ubuntu Desktop - 23.04 - (Ubuntu/Gnome)
> zorin-16.3                       => Zorin Desktop - 16.3
> mint-21.2                        => Mint Desktop - 21.2 - Victoria / XFCE
> manjaro-23.0-230903              => Manjaro Desktop - 23.00230903 - Gnome
> bodhi-7.0.0                      => Bodhi Desktop - 7.0.0 - HWE
> antix-23                         => antiX - 23 - Full
> puppy-9.5-fossa                  => Puppy Linux - 9.5 - Fossa
> kali-2023.3                      => Kali Desktop - 2023.3 - Live
> gentoo-2023-09-03                => Gentoo - 2023-09-03 - Live
> popos-22.04                      => Pop!_OS - 22.04 LTS
> arch-2023.09.01                  => Arch Linux - 2023.09.01 - Live
> rescue-10.1                      => System Rescue - 10.1
> xubuntu-23.04                    => Ubuntu Desktop - 23.04 - (XUbuntu/XFCE)
> kubuntu-23.04                    => Ubuntu Desktop - 23.04 - (KUbuntu/KDE)
> lubuntu-23.04                    => Ubuntu Desktop - 23.04 - (LUbuntu/LXDE)
> bubuntu-23.04                    => Ubuntu Desktop - 23.04 - (Budgie)
> mubuntu-23.04                    => Ubuntu Desktop - 23.04 - (MATE)
> subuntu-23.04                    => Ubuntu Desktop - 23.04 - (Studio)
> fedora-38-gnome                  => Fedora Desktop - 38 / 1.6 - Gnome
```