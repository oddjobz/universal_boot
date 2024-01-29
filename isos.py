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
    'debian-12.1': {
        'name': 'debian',
        'menu': 'debian',
        'title': 'Debian Desktop - 12.1  - Gnome',
        'iso': 'https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.1.0-amd64-gnome.iso',
        'sums': 'https://cdimage.debian.org/debian-cd/current-live/amd64/bt-hybrid/SHA256SUMS',
        'sign': 'https://cdimage.debian.org/debian-cd/current-live/amd64/bt-hybrid/SHA256SUMS.sign',
        'prints': [
            'DF9B9C49EAA9298432589D76DA87E80D6294BE9B'
        ],
        'keyserver': 'keyring.debian.org'
    },
    'ubuntu-23.04': {
        'name': 'ubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop - 23.04 - (Ubuntu/Gnome)',
        'iso': 'https://releases.ubuntu.com/lunar/ubuntu-23.04-desktop-amd64.iso',
        'sums': 'https://releases.ubuntu.com/lunar/SHA256SUMS',
        'sign': 'https://releases.ubuntu.com/lunar/SHA256SUMS.gpg',
        'prints': [
            'C5986B4F1257FFA86632CBA746181433FBB75451',
            '843938DF228D22F7B3742BC0D94AA3F0EFE21092'
        ],
        'keyserver': 'hkp://keyserver.ubuntu.com'
    },
    'zorin-16.3': {
        'name': 'zorin',
        'iso': 'https://mirror.webworld.ie/zorinos/16/Zorin-OS-16.3-Core-64-bit.iso',
        'sums': '58b99c071958c2039f51ddf2e10e7afb483fed3fcef5d91702bcb5db7b9e2432',
        'menu': 'debian-loop',
        'title': 'Zorin Desktop - 16.3'
    },
    'mint-21.2': {
        'name': 'mint',
        'menu': 'debian',
        'title': 'Mint Desktop - 21.2 - Victoria / XFCE', 
        'iso': 'https://mirror.bytemark.co.uk/linuxmint/stable/21.2/linuxmint-21.2-xfce-64bit.iso',
        'sums': 'https://ftp.heanet.ie/mirrors/linuxmint.com/stable/21.2/sha256sum.txt',
        'sign': 'https://ftp.heanet.ie/mirrors/linuxmint.com/stable/21.2/sha256sum.txt.gpg',
    },
    'manjaro-23.0-230903': {
        'name': 'manjaro',
        'menu': 'manjaro',
        'title': 'Manjaro Desktop - 23.00230903 - Gnome',
        'iso': 'https://download.manjaro.org/gnome/23.0/manjaro-gnome-23.0-230903-linux65.iso',
        'sums': 'https://download.manjaro.org/gnome/23.0/manjaro-gnome-23.0-230903-linux65.iso.sha512',
        'sum-size': 512,        
    },
    'bodhi-7.0.0': {
        'name': 'bodhi',
        'menu': 'bodhi',
        'title': 'Bodhi Desktop - 7.0.0 - HWE',
        'iso': 'https://sourceforge.net/projects/bodhilinux/files/7.0.0/bodhi-7.0.0-64-hwe.iso',
        'sums': 'https://altushost-swe.dl.sourceforge.net/project/bodhilinux/7.0.0/bodhi-7.0.0-64-hwe.iso.sha256',
    },
    'antix-23': {
        'name': 'antix',
        'menu': 'antix',
        'title': 'antiX - 23 - Full',
        'iso': 'https://sourceforge.net/projects/antix-linux/files/Final/antiX-23/antiX-23_x64-full.iso',
        'sums': '20fd8f5bf2ef0007b743ceb441db66ae46c4a73fdb9816619fa3211561671524',
    },
    'puppy-9.5-fossa': {
        'name': 'puppy',
        'title': 'Puppy Linux - 9.5 - Fossa',
        'menu': 'puppy',
        'iso': 'https://distro.ibiblio.org/puppylinux/puppy-fossa/fossapup64-9.5.iso',
        'sums': 'https://distro.ibiblio.org/puppylinux/puppy-fossa/fossapup64-9.5.iso.md5.txt',
        'sum-size': 'md5',        
    },
    'kali-2023.3': {
        'name': 'kali',
        'menu': 'debian',
        'title': 'Kali Desktop - 2023.3 - Live',
        'iso': 'https://cdimage.kali.org/kali-2023.3/kali-linux-2023.3-live-amd64.iso',
        'sums': '7755f44318e6183d8411128b8a56c2982dbf0dd4c62870f4e5ca28c6df73fd9a'
    },
    'gentoo-2023-09-03': {
        'name': 'gentoo',
        'title': 'Gentoo - 2023-09-03 - Live',
        'iso': 'https://distfiles.gentoo.org/releases/amd64/autobuilds/20230903T170202Z/livegui-amd64-20230903T170202Z.iso',
        'menu': 'gentoo',
        'hook': fix_gentoo
    },
    'popos-22.04': {
        'name': 'popos',
        'title': 'Pop!_OS - 22.04 LTS',
        'iso': 'https://iso.pop-os.org/22.04/amd64/intel/33/pop-os_22.04_amd64_intel_33.iso',
        'sums': 'ff834c94c6bc970a9508da24fccf32ac829a51030488e612cc1ab4ecf4e0859d',
        'menu': 'debian'        
    },
    'arch-2023.09.01': {
        'name': 'arch',
        'title': 'Arch Linux - 2023.09.01 - Live',
        'iso': 'https://mirror.bytemark.co.uk/archlinux/iso/2023.09.01/archlinux-2023.09.01-x86_64.iso',
        'menu': 'arch',
        'sums': 'https://mirror.bytemark.co.uk/archlinux/iso/2023.09.01/sha256sums.txt',      
    },
    'rescue-10.1': {
        'name': 'rescue',
        'menu': 'debian-loop',
        'title': 'System Rescue - 10.1',
        'iso': 'https://fastly-cdn.system-rescue.org/releases/10.01/systemrescue-10.01-amd64.iso',
        'sums': 'https://www.system-rescue.org/releases/10.01/systemrescue-10.01-amd64.iso.sha256',
        'sign': 'https://www.system-rescue.org/releases/10.01/systemrescue-10.01-amd64.iso.asc',
        'prints': [
            '0FF11AF081E98345594812037091115F8320B897',
            '62989046EB5C7E985ECDF5DD3B0FEA9BE13CA3C9'
        ]       
    },
    'xubuntu-23.04': {
        'name': 'xubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop - 23.04 - (XUbuntu/XFCE)',
        'iso': 'https://cdimages.ubuntu.com/xubuntu/releases/23.04/release/xubuntu-23.04-desktop-amd64.iso',
        'sums': 'https://cdimages.ubuntu.com/xubuntu/releases/23.04/release/SHA256SUMS',
        'sign': 'https://cdimages.ubuntu.com/xubuntu/releases/23.04/release/SHA256SUMS.gpg',
        'prints': [
            'C5986B4F1257FFA86632CBA746181433FBB75451',
            '843938DF228D22F7B3742BC0D94AA3F0EFE21092'
        ]
    },
    'kubuntu-23.04': {
        'name': 'kubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop - 23.04 - (KUbuntu/KDE)',
        'iso': 'https://cdimage.ubuntu.com/kubuntu/releases/23.04/release/kubuntu-23.04-desktop-amd64.iso',
        'sums': 'https://cdimage.ubuntu.com/kubuntu/releases/23.04/release/SHA256SUMS',
        'sign': 'https://cdimage.ubuntu.com/kubuntu/releases/23.04/release/SHA256SUMS.gpg',
        'prints': [
            'C5986B4F1257FFA86632CBA746181433FBB75451',
            '843938DF228D22F7B3742BC0D94AA3F0EFE21092'
        ]        
    },
    'lubuntu-23.04': {
        'name': 'lubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop - 23.04 - (LUbuntu/LXDE)',
        'iso': 'https://cdimage.ubuntu.com/lubuntu/releases/23.04/release/lubuntu-23.04-desktop-amd64.iso',
        'sums': 'https://cdimage.ubuntu.com/lubuntu/releases/23.04/release/SHA256SUMS',
        'sign': 'https://cdimage.ubuntu.com/lubuntu/releases/23.04/release/SHA256SUMS.gpg'
    },
    'bubuntu-23.04': {
        'name': 'bubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop - 23.04 - (Budgie)',
        'iso': 'https://cdimage.ubuntu.com/ubuntu-budgie/releases/23.04/release/ubuntu-budgie-23.04-desktop-amd64.iso',
        'sums': 'https://cdimage.ubuntu.com/ubuntu-budgie/releases/23.04/release/SHA256SUMS',
        'sign': 'https://cdimage.ubuntu.com/ubuntu-budgie/releases/23.04/release/SHA256SUMS.gpg'
    },
    'mubuntu-23.04': {
        'name': 'mubuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop - 23.04 - (MATE)',
        'iso': 'https://cdimage.ubuntu.com/ubuntu-mate/releases/23.04/release/ubuntu-mate-23.04-desktop-amd64.iso',
        'sums': 'https://cdimage.ubuntu.com/ubuntu-mate/releases/23.04/release/SHA256SUMS',
        'sign': 'https://cdimage.ubuntu.com/ubuntu-mate/releases/23.04/release/SHA256SUMS.gpg'
    },
    'subuntu-23.04': {
        'name': 'subuntu',
        'menu': 'debian-loop',
        'title': 'Ubuntu Desktop - 23.04 - (Studio)',
        'iso': 'https://cdimage.ubuntu.com/ubuntustudio/releases/23.04/release/ubuntustudio-23.04-dvd-amd64.iso',
        'sums': 'https://cdimage.ubuntu.com/ubuntustudio/releases/23.04/release/SHA256SUMS',
        'sign': 'https://cdimage.ubuntu.com/ubuntustudio/releases/23.04/release/SHA256SUMS.gpg'        
    },
    'fedora-38-gnome': {
        'name': 'fedora',
        'menu': 'redhat',
        'title': 'Fedora Desktop - 38 / 1.6 - Gnome',
        'iso': 'https://download.fedoraproject.org/pub/fedora/linux/releases/38/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-38-1.6.iso',
        'sums': 'https://download.fedoraproject.org/pub/fedora/linux/releases/38/Workstation/x86_64/iso/Fedora-Workstation-38-1.6-x86_64-CHECKSUM',
        'sign': 'https://fedoraproject.org/fedora.gpg'
    }
}
