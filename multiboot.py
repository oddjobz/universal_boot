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
from argparse import ArgumentParser
from pathlib import Path
from subprocess import call, Popen, PIPE, check_call, run
from urllib import request
from http.cookiejar import CookieJar
from tqdm import tqdm
from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound
from isos import iso_images


class Multiboot:
    
    def __init__ (self):
        self._installed = None
        self._available = None
        self._titles = None
        self._env = Environment(
            loader=PackageLoader("templates"),
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
                return
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
            print (name)
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
            req = request.urlopen(iso)
            CHUNK = 64 * 1024
            with open(path, 'wb') as fp:
                with tqdm(total=req.length/CHUNK+1, desc=iso_name, bar_format="{l_bar}{bar}") as progress:
                    while True:
                        chunk = req.read(CHUNK)
                        if not chunk: break
                        fp.write(chunk)
                        progress.update()
        else:
            print ('* ISO already present, adding to the menu')
        self.gnupg_verify (name)
        
    def gnupg_verify (self, name):
        entry = iso_images[name]
        sign = entry.get('sign')
        sums = entry.get('sums')
        if not sign or not sums:
            print(f"Unable to verify, checksums unavailable")
            return
        cj = CookieJar()
        req = request.Request(sign, headers={'User-Agent': 'Mozilla/5.0'})
        opener = request.build_opener(request.HTTPCookieProcessor(cj))
        response = opener.open(req)
        sign_data = response.read()
        req = request.Request(sums, headers={'User-Agent': 'Mozilla/5.0'})
        opener = request.build_opener(request.HTTPCookieProcessor(cj))
        response = opener.open(req)
        sums_data = response.read()
        with open('/tmp/SHA256SUMS.gpg', 'wb') as io:
            io.write(sign_data)
        with open('/tmp/SHA256SUMS', 'wb') as io:
            io.write(sums_data)
        ret = call([f'gpg --homedir .gnupg --keyid-format long --verify /tmp/SHA256SUMS.gpg /tmp/SHA256SUMS 2>/tmp/SHAERR'], shell=True)
        print (f'Verified => {name}' if not ret else f'ERROR on {entry["name"]}')
        if ret:
            with open('/tmp/SHAERR') as io:
                print(io.read())

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
        args = parser.parse_args()
        
        if args.list:   self.list ()
        if args.add:    self.add (args.add)
        if args.verify: self.verify (args.verify)
        if args.update: self.update ()
        if args.grub:   self.grub ()


if __name__ == '__main__':
    Multiboot().main()
    
