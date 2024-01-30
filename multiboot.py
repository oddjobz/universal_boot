#!/usr/bin/env python3
#############################################################################
#                                                                           #
#   Name: multiboot.py                                                      #
#   Desc: maintenance script for multi-boot USB key                         #
#   Date: July 2023                                                         #
#                                                                           #
#   Version:    0.9                                                         #
#   Author:     Gareth Bult, Mad Penguin Consulting Ltd                     #                                 
#   License:    MIT                                                         #
#                                                                           #
#############################################################################
#
#   TODO:
#   4. Fix init.sh and test from key
#
#############################################################################
import rainbow_tqdm 
import hashlib
from argparse import ArgumentParser
from pathlib import Path
from subprocess import call, Popen, PIPE, check_call, run
from tqdm import tqdm
from pycurl import Curl
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound
from isos import iso_images
from os import rename
from whiptail import Whiptail


class Multiboot:
    
    def __init__ (self):
        self._installed = None
        self._available = None
        self._titles = None
        self._env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape()
        )

    def read_isos (self):
        self._installed = {}
        self._available = {}
        self._titles = {}
        for iso in Path('isos').iterdir():
            iso = iso.as_posix().split("/")[-1]
            for name, image in iso_images.items():
                entry_iso = image.get('iso').split('/')[-1]
                if iso == entry_iso:
                    break
            else:
                print (f'Unknown ISO: {iso}')
                continue
            if iso:
                self._installed[name] = iso            
                self._titles[name] = image.get('title')
                    
        for name, image in iso_images.items():
            iso = image.get('iso').split('/')[-1]
            if name not in self._installed:
                self._available[name] = iso
                self._titles[name] = image.get('title')

    def list (self):
        self.read_isos ()
        print ("ISO's Present on the USB Key:")
        for name in self._installed:
            print (f'> {name:32} => {self._titles[name]}')
        print ()
        print ("ISO's Available for download:")
        for name in self._available:
            print (f'> {name:32} => {self._titles[name]}')
        print ()
        
    def add (self, name):
        self.read_isos ()
        if name in self._installed:
            print(f'"{name}" is already available!')
            return
        if name not in self._available:
            print(f'"{name}" is not currently available!')
            return
        self.download(name)

    def verify (self, name):
        self.read_isos ()
        if name not in self._installed:
            print(f'"{name}" is not currently available, add it first!')
            return
        self.gnupg_verify (name)
        
    def update (self):
        for name, entry in iso_images.items():
            if 'keyserver' in entry:
                for key in entry.get('prints', []):
                    self.update_key(entry['keyserver'], key)
    
    def grub (self):
        self.read_isos ()
        with open('grub.cfg', 'w') as dst:
            with open('config/grub.cfg', 'r') as src:
                txt = src.read()
                dst.write(txt)
                for name in self._installed:
                    entry = iso_images[name]
                    dst.write('\n')
                    path = f'{entry["menu"]}.jinja2'
                    try:
                        if 'filename' not in entry:
                            entry['filename'] = entry['iso'].split('/')[-1]
                        template = self._env.get_template(path)
                        txt = template.render(**entry)
                        dst.write(txt)
                    except TemplateNotFound:
                        print(f"ERROR: template missing: {path}")
        #
        #   TODO: now copy grub.cfg onto boot partition for USB key
        #
        p = Popen([f'blkid','--label','MP-DATA'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if p.returncode:
            print(f'* Error: {err} - unable to re-write GRUB')
        else:
            device = output.decode().split('\n')[0]
            Path('/media/data').mkdir(exist_ok=True, parents=True)
            check_call(['mount', device, '/media/data'])
            src = Path('grub.cfg')
            dst = Path('/media/data/boot/grub/grub.cfg')
            dst.write_text(src.read_text())
            check_call(['umount', device])

    def gui (self):
        self.read_isos ()
        lines = []
        installed = list(self._installed)
        installed.sort()
        for name in installed:
            title = iso_images[name]['title'].replace(' ', '-')
            lines.append((name, title, 'ON'))
        available = list(self._available)
        available.sort()
        for name in available:
            title = iso_images[name]['title'].replace(' ', '-')
            lines.append((name, title, 'OFF'))

        w = Whiptail(title="Currently Active USB ISO Images")
        response = w.checklist('\n Choose which images should be included, use space bar to select', lines, prefix="")
        if response[1]:
            print ('* GUI Cancelled')
            return
        wanted = set(response[0])
        existing = set(self._installed)
        to_install = wanted.difference(existing)
        to_delete = existing.difference(wanted)
        if not to_delete and not to_install:
            print ("* No changes requested")
            return
        w = Whiptail(title="Install / Remove ISO's")
        d = ''
        for x in to_delete:
            d += f'* {x}\n'
        i = ''
        for x in to_install:
            i += f'* {x}\n'
        prompt = ''
        if d:
            prompt += "ISO's to be deleted:\n" + d + '\n'
        if i:
            prompt += "ISO's to downloaded:\n" + i + '\n'
        if d:
            prompt += "If you delete ISO's you will need to download them again if you wish to use them.\n"
        if i:
            prompt += "Downloading will take time, don't turn your computer or your Internet connection off while downloading.\n"
        prompt += '\nAre you sure you want to do this?'
        w.calc_height(prompt)
        if not w.yesno(prompt, 'no'):
            for item in to_delete:
                print (f"* Delete: {item}")
            for item in to_install:
                print (f"* Download: {item}")

    def update_key (self, server, key):
        print (f'Updating "{key}" using keyserver "{server}"')
        ret = call([f'gpg --homedir .gnupg --keyid-format long --keyserver {server} --recv-keys {key} 2>/tmp/SHAERR'], shell=True)
        if ret:
            with open('/tmp/SHAERR') as io:
                print(io.read())

    def download (self, name):
        entry = iso_images[name]
        iso = entry['iso']
        iso_name = iso.split('/')[-1]
        path = Path(f'isos/{iso_name}')
        if not path.exists():
            print(f"Need to download: {entry['iso']}")
            self.download_file (iso, iso_name)
            rename (f'tmp/{iso_name}', f'isos/{iso_name}')
        else:
            print ('* ISO already present, adding to the menu')
        self.gnupg_verify (name)
        
    def download_file (self, iso, path=None):
        if not path:
            path = iso.split('/')[-1]
        Path('tmp').mkdir(exist_ok=True)            
        with tqdm (total=9e9, unit='iB', unit_scale=True) as progress:

            total_dl_d = [0]

            def status (download_t, download_d, upload_t, upload_d, total=total_dl_d):
                if progress.total != download_t:
                    progress.reset(download_t)    
                progress.update(download_d - total[0])
                total[0] = download_d
            
            with open(f'tmp/{path}', 'wb') as f:
                c = Curl()
                c.setopt(c.URL, iso)
                c.setopt(c.FOLLOWLOCATION, True)
                c.setopt(c.WRITEDATA, f)
                c.setopt(c.NOPROGRESS, False)
                c.setopt(c.XFERINFOFUNCTION, status)
                c.perform()
                c.close()

    def gnupg_verify (self, name):
        entry = iso_images[name]
        sign = entry.get('sign')
        sums = entry.get('sums')
        if not sign or not sums:
            print(f"Unable to verify, checksums unavailable")
            return
        filename = entry["iso"].split('/')[-1]
        self.download_file (sign)
        self.download_file (sums)
        ret = call([f'gpg --homedir .gnupg --keyid-format long --verify tmp/SHA256SUMS.sign tmp/SHA256SUMS 2>/tmp/SHAERR'], shell=True)
        if ret:
            print (f'* ERROR on {name} - SHA256SUMS corrupt')
            if ret:
                with open('/tmp/SHAERR') as io:
                    print(io.read())
            return
        print ("Checking signature ...")
        path = Path(f'tmp/{filename}')
        if not path.exists():
            path = Path(f'isos/{filename}')
            if not path.exists():
                print(f"* File not available: {filename}")
                return
        csum = self.checksum(path)
        with open ('tmp/SHA256SUMS') as io:
            while line := io.readline().strip('\n'):
                sign, file = [word for word in line.split(' ') if word]
                if file == filename:
                    if sign == csum:
                        print(f'* Signature OK')
                    else:
                        print(f'* Signature BAD')
                    return
        print(f"* No such file listed: {file}")
        
    def checksum(self, path, hash_factory=hashlib.sha256, chunk_num_blocks=16384):
        h = hash_factory()
        size = path.stat().st_size
        with open(path.as_posix(),'rb') as f:
            with tqdm(total=size/(chunk_num_blocks*h.block_size)+1, desc=path.as_posix(), bar_format="{l_bar}{bar}") as progress:
                while chunk := f.read(chunk_num_blocks*h.block_size): 
                    h.update(chunk)
                    progress.update()
        return h.hexdigest()

    def main (self):
        parser = ArgumentParser(
            prog="multiboot.py",
            description="USB Key Maintenance",
            epilog='Free Software for Linux from Mad Penguin Consulting Ltd')
        
        parser.add_argument("--list", action='store_true', help="List available ISO's")
        parser.add_argument("--update", action='store_true', help="Update software and signatures")
        parser.add_argument("--add", type=str, metavar="<iso>", help="The name of the ISO to add")
        parser.add_argument("--verify", type=str, metavar="<iso>", help="Verify the ISO's signatures")
        parser.add_argument("--grub", action='store_true', help="Refresh the GRUB boot information")
        parser.add_argument("--gui", action='store_true', help="Fire up the text based GUI")
        args = parser.parse_args()

        if args.gui:
            return self.gui ()
        action = False
        if args.list:
            self.list ()
            action = True
        if args.add:
            self.add (args.add)
            action = True
        if args.verify:
            self.verify (args.verify)
            action = True
        if args.update:
            self.update ()
            action = True
        if args.grub:
            self.grub ()
            action = True
        if args.isos_update:
            self.isos_update (args.isos_update)
            action = True
        if not action:
            print ('No action specified, try adding --help')


if __name__ == '__main__':
    Multiboot().main()
    
