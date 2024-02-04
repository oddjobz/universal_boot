from pathlib import Path
from shutil import move
from subprocess import call

def fix_gentoo (entry):
    if Path('/media/data/boot/gentoo/image.squashfs').exists():
        return
    print ('Running the Gentoo fix')
    # name = entry['iso'].split('/')[-1]
    # if Path(f'isos/{name}').exists() and not Path(f'./{name}').exists():
    #     move(f'isos/{name}', f'./{name}')
    #     with open(f'isos/{name}', 'w') as io:
    #         io.write('Moved\n')

    # call([f'sudo mkdir -p /media/data/boot/gentoo'], shell=True)          
    # call([f'sudo mkdir -p /mnt/loop'], shell=True)          
    # call([f'sudo mount -o loop ./{name} /mnt/loop'], shell=True)  
    # call([f'sudo cp /mnt/loop/boot/gentoo /media/data/boot/gentoo/gentoo'], shell=True)
    # call([f'sudo cp /mnt/loop/boot/gentoo.igz /media/data/boot/gentoo/gentoo.igz'], shell=True)
    # call([f'sudo cp /mnt/loop/image.squashfs /media/data/boot/gentoo/image.squashfs'], shell=True)
    # call([f'sudo umount /mnt/loop'], shell=True)

iso_images = {
    'debian-12.04-cinnamon': {
        'name': 'debian',
        'menu': 'debian',
        'title': 'Debian Desktop (12.04) Cinnamon',
        'size': 3.1,
        'iso': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-cinnamon.iso',
        'sums': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS',
        'sign': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS.sign',
        'prints': [
            'DF9B9C49EAA9298432589D76DA87E80D6294BE9B'
        ],
        'keyserver': 'keyring.debian.org'
    },
    'debian-12.04-gnome': {
        'name': 'debian',
        'menu': 'debian',
        'title': 'Debian Desktop (12.04) Gnome',
        'size': 3.2,
        'iso': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-gnome.iso',
        'sums': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS',
        'sign': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS.sign',
        'prints': [
            'DF9B9C49EAA9298432589D76DA87E80D6294BE9B'
        ],
        'keyserver': 'keyring.debian.org'
    },
    'debian-12.04-kde': {
        'name': 'debian',
        'menu': 'debian',
        'title': 'Debian Desktop (12.04) KDE',
        'size': 3.3,
        'iso': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-kde.iso',
        'sums': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS',
        'sign': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS.sign',
        'prints': [
            'DF9B9C49EAA9298432589D76DA87E80D6294BE9B'
        ],
        'keyserver': 'keyring.debian.org'
    },
    'debian-12.04-lxde': {
        'name': 'debian',
        'menu': 'debian',
        'title': 'Debian Desktop (12.04) LXDE',
        'size': 2.9,
        'iso': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-lxde.iso',
        'sums': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS',
        'sign': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS.sign',
        'prints': [
            'DF9B9C49EAA9298432589D76DA87E80D6294BE9B'
        ],
        'keyserver': 'keyring.debian.org'
    },
    'debian-12.04-lxqt': {
        'name': 'debian',
        'menu': 'debian',
        'title': 'Debian Desktop (12.04) LXQT',
        'size': 3.0,
        'iso': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-lxqt.iso',
        'sums': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS',
        'sign': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS.sign',
        'prints': [
            'DF9B9C49EAA9298432589D76DA87E80D6294BE9B'
        ],
        'keyserver': 'keyring.debian.org'
    },
    'debian-12.04-mate': {
        'name': 'debian',
        'menu': 'debian',
        'title': 'Debian Desktop (12.04) MATE',
        'size': 3.0,
        'iso': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-mate.iso',
        'sums': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS',
        'sign': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS.sign',
        'prints': [
            'DF9B9C49EAA9298432589D76DA87E80D6294BE9B'
        ],
        'keyserver': 'keyring.debian.org'
    },
    'debian-12.04-standard': {
        'name': 'debian',
        'menu': 'debian',
        'title': 'Debian Desktop (12.04) Standard',
        'size': 1.4,
        'iso': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-standard.iso',
        'sums': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS',
        'sign': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS.sign',
        'prints': [
            'DF9B9C49EAA9298432589D76DA87E80D6294BE9B'
        ],
        'keyserver': 'keyring.debian.org'
    },
    'debian-12.04-xfce': {
        'name': 'debian',
        'menu': 'debian',
        'title': 'Debian Desktop (12.04) XFCE',
        'size': 3.0,
        'iso': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-xfce.iso',
        'sums': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS',
        'sign': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/SHA256SUMS.sign',
        'prints': [
            'DF9B9C49EAA9298432589D76DA87E80D6294BE9B'
        ],
        'keyserver': 'keyring.debian.org'
    },
    'sparky-07.02-lxqt': {
        'name': 'sparky',
        'menu': 'sparky',
        'title': 'Sparky Desktop (07.02) LXQt',
        'size': 1.79,
        'iso': 'https://sourceforge.net/projects/sparkylinux/files/lxqt/sparkylinux-7.2-x86_64-lxqt.iso',
        'sum': 'ca66cbf2c648f133c10be3d3a912ef299b6fe276a4dce59cb7228e3731830ea5'
    },
    'sparky-07.02-mate': {
        'name': 'sparky',
        'menu': 'sparky',
        'title': 'Sparky Desktop (07.02) Mate',
        'size': 1.98,
        'iso': 'https://sourceforge.net/projects/sparkylinux/files/mate/sparkylinux-7.2-x86_64-mate.iso',
        'sums': 'https://sourceforge.net/projects/sparkylinux/files/lxqt/sparkylinux-7.2-x86_64-lxqt.iso.allsums.txt',
        'sign': 'https://sourceforge.net/projects/sparkylinux/files/mate/sparkylinux-7.2-x86_64-mate.iso.sig',
    },
    'sparky-07.02-xfce': {
        'name': 'sparky',
        'menu': 'sparky',
        'title': 'Sparky Desktop (07.02) XFCE',
        'size': 1.63,
        'iso': 'https://sourceforge.net/projects/sparkylinux/files/xfce/sparkylinux-7.2-x86_64-xfce.iso',
        'sums': 'https://sourceforge.net/projects/sparkylinux/files/xfce/sparkylinux-7.2-x86_64-xfce.iso.allsums.txt',
        'sign': 'https://sourceforge.net/projects/sparkylinux/files/xfce/sparkylinux-7.2-x86_64-xfce.iso.sig',
    },
    'sparky-07.02-kde': {
        'name': 'sparky',
        'menu': 'sparky',
        'title': 'Sparky Desktop (07.02) KDE',
        'size': 2.09,
        'iso': 'https://sourceforge.net/projects/sparkylinux/files/kde/sparkylinux-7.2-x86_64-kde.iso',
        'sums': 'https://sourceforge.net/projects/sparkylinux/files/kde/sparkylinux-7.2-x86_64-kde.iso.allsums.txt',
        'sign': 'https://sourceforge.net/projects/sparkylinux/files/kde/sparkylinux-7.2-x86_64-kde.iso.sig',
    },
    'sparky-07.02-minimal': {
        'name': 'sparky',
        'menu': 'sparky',
        'title': 'Sparky Desktop (07.02) Minimal',
        'size': 1.39,
        'iso': 'https://sourceforge.net/projects/sparkylinux/files/base/sparkylinux-7.2-x86_64-minimalgui.iso',
        'sums': 'https://sourceforge.net/projects/sparkylinux/files/base/sparkylinux-7.2-x86_64-minimalgui.iso.allsums.txt',
        'sign': 'https://sourceforge.net/projects/sparkylinux/files/base/sparkylinux-7.2-x86_64-minimalgui.iso.sig',
    },
    'sparky-07.02-min-i686': {
        'name': 'sparky',
        'menu': 'sparky',
        'title': 'Sparky Desktop (07.02) Min (i686)',
        'size': 1.21,
        'iso': 'https://sourceforge.net/projects/sparkylinux/files/base/sparkylinux-7.2-i686-minimalgui.iso',
        'sums': 'https://sourceforge.net/projects/sparkylinux/files/base/sparkylinux-7.2-i686-minimalgui.iso.allsums.txt',
        'sign': 'https://sourceforge.net/projects/sparkylinux/files/base/sparkylinux-7.2-i686-minimalgui.iso.sig',
    },
    'sparky-07.02-cli-i686': {
        'name': 'sparky',
        'menu': 'sparky',
        'title': 'Sparky Desktop (07.02) CLI (i686)',
        'size': 0.717,
        'iso': 'https://sourceforge.net/projects/sparkylinux/files/cli/sparkylinux-7.2-i686-minimalcli.iso',
        'sums': 'https://sourceforge.net/projects/sparkylinux/files/cli/sparkylinux-7.2-i686-minimalcli.iso.allsums.txt',
        'sign': 'https://sourceforge.net/projects/sparkylinux/files/cli/sparkylinux-7.2-i686-minimalcli.iso.sig',
    },


    'ubuntu-22.04': {
        'name': 'ubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop (22.04) Gnome',
        'size': 4.7,
        'iso': 'https://releases.ubuntu.com/lunar/ubuntu-22.04.3-desktop-amd64.iso',
        'sum': 'a435f6f393dda581172490eda9f683c32e495158a780b5a1de422ee77d98e909'
    },
    'ubuntu-23.04': {
        'name': 'ubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop (23.04) Gnome',
        'size': 4.6,
        'iso': 'https://releases.ubuntu.com/lunar/ubuntu-23.04-desktop-amd64.iso',
        'sums': 'https://releases.ubuntu.com/lunar/SHA256SUMS',
        'sign': 'https://releases.ubuntu.com/lunar/SHA256SUMS.gpg',
        'prints': [
            '843938DF228D22F7B3742BC0D94AA3F0EFE21092'
        ],
        'keyserver': 'hkp://keyserver.ubuntu.com'
    },
    'ubuntu-23.04-xfce': {
        'name': 'xubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop (23.04) XFCE',
        'size': 2.9,
        'iso': 'https://www.mirrorservice.org/sites/cdimage.ubuntu.com/cdimage/xubuntu/releases/22.04/release/xubuntu-22.04.3-desktop-amd64.iso',
        'sum': 'eec14c4e6f13120555fee0f1f3c1909bd8196a48de4012b6ea96fb7dd27a5aab',
    },
    'ubuntu-23.04-kde': {
        'name': 'kubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop (23.04) KDE',
        'size': 4.0,
        'iso': 'https://cdimage.ubuntu.com/kubuntu/releases/22.04.3/release/kubuntu-22.04.3-desktop-amd64.iso',
        'sum': '9a5ea3b4ae6651cf0cd82ec059e3e5c8d8b30006112ff06555acb35e45571f50',
    },
    'ubuntu-23.04-lxde': {
        'name': 'lubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop (23.04) LXDE',
        'size': 2.8,
        'iso': 'https://cdimage.ubuntu.com/lubuntu/releases/22.04.3/release/lubuntu-22.04.3-desktop-amd64.iso',
        'sum': 'ffccfa53a10bacf0b8b7589e85c739e650aef8f38ac4ed66f96fd591396d2f21',
    },
    'ubuntu-23.04-budgie': {
        'name': 'bubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop (23.04) Budgie',
        'size': 3.5,
        'iso': 'https://cdimage.debian.org/mirror/cdimage.ubuntu.com/ubuntu-budgie/releases/22.04.3/release/ubuntu-budgie-22.04.3-desktop-amd64.iso',
        'sum': '03e8fa55a8634cf61fff0c22169576d590b606db568bffae2907ad98278d35b9',
    },
    'ubuntu-23.04-mate': {
        'name': 'mubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop (23.04) MATE',
        'size': 3.5,
        'iso': 'https://cdimage.ubuntu.com/ubuntu-mate/releases/22.04/release/ubuntu-mate-22.04.3-desktop-amd64.iso',
        'sum': 'd84cd3eb7732fbb39ce3cd24ba1b302a643fe0362f7ac9261fc4c7b756e42a55'
    },
    'ubuntu-23.04-studio': {
        'name': 'subuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop (23.04) Studio',
        'size': 4.7,
        'iso': 'https://cdimage.ubuntu.com/ubuntustudio/releases/22.04.3/release/ubuntustudio-22.04.3-dvd-amd64.iso',
        'sums': 'https://cdimage.ubuntu.com/ubuntustudio/releases/22.04.3/release/SHA256SUMS',
        'sign': 'https://cdimage.ubuntu.com/ubuntustudio/releases/22.04.3/release/SHA256SUMS.gpg',
        'keyserver': 'hkp://keyserver.ubuntu.com'        
    },    
    'mint-21.3-cinnamon': {
        'name': 'mint',
        'menu': 'debian',
        'title': 'Mint Desktop (21.03) Cinnamon', 
        'size': 2.9,
        'iso': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.3/linuxmint-21.3-cinnamon-64bit.iso',
        'sums': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.3/sha256sum.txt',
        'sign': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.3/sha256sum.txt.gpg',
        'keyserver': 'hkp://keyserver.ubuntu.com',
        'prints': ['27DEB15644C6B3CF3BD7D291300F846BA25BAE09']
    },
    'mint-21.3-mate': {
        'name': 'mint',
        'menu': 'debian',
        'title': 'Mint Desktop (21.03) Mate', 
        'size': 3.0,
        'iso': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.3/linuxmint-21.3-mate-64bit.iso',
        'sums': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.3/sha256sum.txt',
        'sign': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.3/sha256sum.txt.gpg',
    },
    'mint-21.3-xfce': {
        'name': 'mint',
        'menu': 'debian',
        'title': 'Mint Desktop (21.03) XFCE', 
        'size': 2.9,
        'iso': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.3/linuxmint-21.3-xfce-64bit.iso',
        'sums': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.3/sha256sum.txt',
        'sign': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.3/sha256sum.txt.gpg',
    },
    'bodhi-7.0.0-standard': {
        'name': 'bodhi',
        'menu': 'bodhi',
        'title': 'Bodhi Desktop (7.0.0) Standard',
        'size': 1.3,
        'iso': 'https://sourceforge.net/projects/bodhilinux/files/7.0.0/bodhi-7.0.0-64.iso',
        'sums': 'https://sourceforge.net/projects/bodhilinux/files/7.0.0/bodhi-7.0.0-64.iso.sha256',
    },
    'bodhi-7.0.0-hwe': {
        'name': 'bodhi',
        'menu': 'bodhi',
        'title': 'Bodhi Desktop (7.0.0) HWE',
        'size': 1.3,
        'iso': 'https://sourceforge.net/projects/bodhilinux/files/7.0.0/bodhi-7.0.0-64-hwe.iso',
        'sums': 'https://sourceforge.net/projects/bodhilinux/files/7.0.0/bodhi-7.0.0-64-hwe.iso.sha256'
    },
    'arch-2024.02.01': {
        'name': 'arch',
        'menu': 'arch',
        'title': 'Arch Linux (2024.01.01) Live',
        'size': 0.93,
        'iso': 'https://mirror.bytemark.co.uk/archlinux/iso/2024.02.01/archlinux-2024.02.01-x86_64.iso',
        'sum': '891ebab4661cedb0ae3b8fe15a906ae2ba22e284551dc293436d5247220933c5',
    },
    #
    #   FIXME: bad key
    #
    'rescue-11.0': {
        'name': 'rescue',
        'menu': 'debian-loop',
        'title': 'System Rescue (11.0)',
        'size': 0.86,
        'iso': 'https://fastly-cdn.system-rescue.org/releases/11.00/systemrescue-11.00-amd64.iso',
        'sum': 'b25579c9e8814eed84ec3260fa10566cf979e1569f857fa8fe15505968b527ed'
    },
    'zorin-17.0': {
        'name': 'zorin',
        'menu': 'debian-loop',
        'title': 'Zorin Desktop (17.0)',
        'size': 3.6,
        'iso': 'https://mirror.webworld.ie/zorinos/17/Zorin-OS-17-Core-64-bit.iso',
        'sum': '0191e343586d40e1fdaa90dddae0b8c2105223babb63640c05daf29881a4ccfd',
    },
    'antix-23-full-64': {
        'name': 'antix',
        'menu': 'antix',
        'title': 'antiX (23) Full 64-bit',
        'size': 1.7,
        'iso': 'https://sourceforge.net/projects/antix-linux/files/Final/antiX-23/antiX-23_x64-full.iso',
        'sum': '20fd8f5bf2ef0007b743ceb441db66ae46c4a73fdb9816619fa3211561671524'
    },
    'antix-23-full-32': {
        'name': 'antix',
        'menu': 'antix',
        'title': 'antiX (23) Full 32-bit',
        'size': 1.7,
        'iso': 'https://sourceforge.net/projects/antix-linux/files/Final/antiX-23/antiX-23_386-full.iso',
        'sum': '551165bf52bf851b0763e1347c6bff23ba19bea833c2e1d107a9b984ba0a4585'
    },
    'puppy-9.5-fossa': {
        'name': 'puppy',
        'menu': 'puppy',
        'title': 'Puppy Linux (9.5) Fossa',
        'size': 0.41,
        'iso': 'https://distro.ibiblio.org/puppylinux/puppy-fossa/fossapup64-9.5.iso',
        'sf': 'https://distro.ibiblio.org/puppylinux/puppy-fossa/fossapup64-9.5.iso.sha256.txt',
    },
    'kali-2023.4': {
        'name': 'kali',
        'menu': 'debian',
        'title': 'Kali Desktop (2023.4) Live',
        'size': 4.0,
        'iso': 'https://cdimage.kali.org/kali-2023.4/kali-linux-2023.4-installer-amd64.iso',
        'sum': '49f6826e302659378ff0b18eda28121dad7eeab4da3b8d171df034da4996a75e'
    },
    'popos-22.04': {
        'name': 'popos',
        'title': 'Pop!_OS (22.04) LTS',
        'size': 2.5,
        'iso': 'https://iso.pop-os.org/22.04/amd64/intel/33/pop-os_22.04_amd64_intel_33.iso',
        'sum': 'ff834c94c6bc970a9508da24fccf32ac829a51030488e612cc1ab4ecf4e0859d',
        'menu': 'debian'        
    },
    'fedora-38-gnome': {
        'name': 'fedora',
        'menu': 'redhat',
        'title': 'Fedora Desktop (38/1.6) Gnome',
        'size': 2.1,
        'iso': 'https://download.fedoraproject.org/pub/fedora/linux/releases/38/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-38-1.6.iso',
        'sums': 'https://download.fedoraproject.org/pub/fedora/linux/releases/38/Workstation/x86_64/iso/Fedora-Workstation-38-1.6-x86_64-CHECKSUM',
        'sign': 'https://fedoraproject.org/fedora.gpg'
    },
    #
    #   Check for boot menu
    #
    'open-mandriva-5': {
        'name': 'mandriva',
        'menu': 'debian',
        'title': 'Open Mandriva V (23.08) Gnome',
        'size': 2.7,
        'iso': 'https://sourceforge.net/projects/openmandriva/files/release/5.0/openmandriva.5.0-gnome.x86_64.iso',
        'sf': 'https://sourceforge.net/projects/openmandriva/files/release/5.0/openmandriva.5.0-gnome.x86_64.iso.sha256',

    },
    # FIXME: image validation is non-standard, needs work
    # 'gentoo-2023-09-03': {
    #     'name': 'gentoo',
    #     'title': 'Gentoo (2024-01-28) Live',
    #     'iso': 'https://distfiles.gentoo.org/releases/amd64/autobuilds/current-livegui-amd64/livegui-amd64-20240128T165521Z.iso',
    #     'sign': 'https://distfiles.gentoo.org/releases/amd64/autobuilds/current-livegui-amd64/livegui-amd64-20240121T170320Z.iso.asc',
    #     'sums': 'https://distfiles.gentoo.org/releases/amd64/autobuilds/current-livegui-amd64/livegui-amd64-20240128T165521Z.iso.sha256',
    #     'menu': 'gentoo',
    #     'hook': fix_gentoo,
    #     'prints': ['534E4209AB49EEE1C19D96162C44695DB9F6043D'],
    #     'keyserver': 'hkp://keys.openpgp.org',
    # },
    #
    'manjaro-23.1.3': {
        'name': 'manjaro',
        'menu': 'manjaro',
        'title': 'Manjaro Desktop (23.1.3) Gnome',
        'size': 3.9,
        'iso': 'https://download.manjaro.org/gnome/23.1.3/manjaro-gnome-23.1.3-240113-linux66.iso',
        'sum': 'eea2f3163582fb5dc618fe0b15202ba1507449095f25ac43f8a1cf78814201f9'
    },
    'kmanjaro-23.1.3': {
        'name': 'manjaro',
        'menu': 'manjaro',
        'title': 'Manjaro Desktop (23.1.3) KDE',
        'size': 3.7,
        'iso': 'https://download.manjaro.org/kde/23.1.3/manjaro-kde-23.1.3-240113-linux66.iso',
        'sum': 'bb7c43db4ae1c9d7a50a15d635e8144570bfc2000d9aaf35af79c9a916efa158',
    },
    'xmanjaro-23.1.3': {
        'name': 'manjaro',
        'menu': 'manjaro',
        'title': 'Manjaro Desktop (23.1.3) XFCE',
        'size': 3.6,
        'iso': 'https://download.manjaro.org/xfce/23.1.3/manjaro-xfce-23.1.3-240113-linux66.iso',
        'sum': '2709aafc15ea39c45545ab09baf9c567e82ee903b9f1c7a945cf93f216bca75c',
    },
}
