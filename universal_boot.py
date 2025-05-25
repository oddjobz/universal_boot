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
#   4. Fix init.sh and test from key
#
#############################################################################
import rainbow_tqdm 
import hashlib
from argparse import ArgumentParser
from pathlib import Path
from subprocess import call, Popen, PIPE, check_call, run
from tqdm import tqdm
from pycurl import Curl, CAINFO
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound
from isos import iso_images
from os import rename
from datetime import datetime
from whiptail import Whiptail
from psutil import disk_usage


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
        if not Path('isos').exists():
            Path('isos').symlink_to('../boot/iso')

        self._installed = {}
        self._available = {}
        self._verified = set()
        self._titles = {}
        for path in Path('isos').iterdir():
            iso = path.as_posix().split("/")[-1]
            for name, image in iso_images.items():
                entry_iso = image.get('iso').split('/')[-1]
                if iso == entry_iso:
                    break
            else:
                print (f'Unknown ISO: {iso}')
                w = Whiptail(title="Unknown ISO found")
                menu = w.menu(
                    f"The Bootloader doesn't recognise file: {iso}",
                    (('ignore','Ignore this file'), ('delete','Remove this file')))[0]
                if menu == 'delete':
                    print("Delete> ", path)
                    path.unlink()
                continue
            if iso:
                self._installed[name] = iso            
                self._titles[name] = image.get('title')
                if Path(f'verified/{name}').exists():
                    self._verified.add(name)
                    
        for name, image in iso_images.items():
            iso = image.get('iso').split('/')[-1]
            if name not in self._installed:
                self._available[name] = iso
                self._titles[name] = image.get('title')

    def list_print (self, name):
        # print (f'> {name:24} | {"verified  " if name in self._verified else "unverified"} => {self._titles[name]}')
        entry = iso_images[name]
        if name not in self._verified:
            verified = '           '
        elif entry.get('sign'):
            verified = 'Verified ✅'
        elif entry.get('sum'):
            verified = 'By Host  ☑️ '
        else:
            verified = 'By Sum   ⚠️ '
        # verified = "verified  " if name in self._verified else "unverified"
        size = entry.get('size', 0)
        print (f'> {name:24} | {verified} | {size:0.2f}G | {self._titles[name]}')

    def list (self):
        self.read_isos ()
        print ("ISO's Present on the USB Key:")
        installed = list(self._installed)
        installed.sort()
        for name in installed:
            self.list_print(name)
            # print (f'> {name:24} | {"verified  " if name in self._verified else "unverified"} => {self._titles[name]}')
        print ()
        print ("ISO's Available for download:")
        available = list(self._available)
        available.sort()
        for name in self._available:
            self.list_print(name)
            # print (f'> {name:24} | {"verified  " if name in self._verified else "unverified"} => {self._titles[name]}')
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
        if name == "all":
            for name in self._installed:
                self.gnupg_verify (name)    
        else:
            if name not in self._installed:
                print("Name>", name)
                print("Installed>", self._installed)
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

                installed = list(self._installed)
                installed.sort()
                for name in installed:
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
        #   FIXME: now copy grub.cfg onto boot partition for USB key
        #
        if not Path('/usr/sbin/blkid').exists():
            print ('* blkid tool not available')
            return
        p = Popen([f'/usr/sbin/blkid','--label','MP-DATA'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if p.returncode:
            print(f'* Error: {err} - unable to re-write GRUB')
        else:
            device = output.decode().split('\n')[0]
            Path('/media/data').mkdir(exist_ok=True, parents=True)
            try:
                check_call(['mount', device, '/media/data'])
                src = Path('grub.cfg')
                dst = Path('/media/data/boot/grub/grub.cfg')
                dst.write_text(src.read_text())
                check_call(['umount', device])
                print (f'* Upddated!')
            except Exception as e:
                print (f'* ERROR: Error updating key, you are probably not root! => {str(e)}')

    def gui (self):
        self.read_isos ()
        lines = []
        installed = list(self._installed)
        installed.sort()
        for name in installed:
            title = iso_images[name]['title'].replace(' ', '-')
            size = iso_images[name].get('size', 0)
            lines.append((name, f'{size:4}G| {title}', 'ON'))
        available = list(self._available)
        available.sort()
        for name in available:
            title = iso_images[name]['title'].replace(' ', '-')
            size = iso_images[name].get('size', 0)
            lines.append((name, f'{size:4}G| {title}', 'OFF'))

        fs = disk_usage('isos')
        d = 10000000
        size = int(fs.total/d)/100
        used = int(fs.used/d)/100
        free = int(fs.free/d)/100
        spc = 'Key size: {}G, %used: {}, used: {}G, free: {}G'.format(size, fs.percent, used, free)

        w = Whiptail(title="Currently Active USB ISO Images")
        response = w.checklist(f'Choose which images should be included, use space bar to select\n{spc}', lines, prefix="")
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
        del_size = 0
        for x in to_delete:
            d += f'* {x}\n'
            del_size += iso_images[x].get('size', 0)
        i = ''

        add_size = 0
        for x in to_install:
            i += f'* {x}\n'
            add_size += iso_images[x].get('size', 0)
        prompt = ''
        if d:
            prompt += "ISO's to be deleted:\n" + d + '\n'
        if i:
            prompt += "ISO's to downloaded:\n" + i + '\n'
        if d:
            prompt += "If you delete ISO's you will need to download them again if you wish to use them.\n"
        if i:
            prompt += "Downloading will take time, don't turn your computer or your Internet connection off while downloading.\n"

        add_size = int(add_size*100)/100
        del_size = int(del_size*100)/100
        net_size = int((add_size - del_size)*100)/100

        prompt += f'\nRemove {del_size}G and Download {add_size}G, net change {net_size}G, free {free}G'
        prompt += '\nAre you sure you want to do this?'
        if net_size + 1 > free:
            prompt += '\nWARNING: THIS DOWNLOAD MAY NOT FIT ON YOUR KEY!'
        w.calc_height(prompt)
        if not w.yesno(prompt, 'no'):
            for name in to_delete:
                print (f"* Delete: {name}")
                entry = iso_images[name]
                iso = entry['iso']
                iso_name = iso.split('/')[-1]
                Path(f'isos/{iso_name}').unlink()
            for item in to_install:
                print (f"* Download: {item}")
                self.download (item)
            print("<< Updating the Bootloader GRUB Configuration >>")
            self.grub()

    def update_key (self, server, key):
        print (f'Updating "{key}" using keyserver "{server}"')
        ret = call([f'gpg --keyid-format long --keyserver {server} --recv-keys {key} 2>/tmp/SHAERR'], shell=True)
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
            if self.download_file (iso, iso_name):
                rename (f'tmp/{iso_name}', f'isos/{iso_name}')
            else:
                print (f'* ERROR: ISO download failed! => {iso}')
                return
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

            if 'sourceforge' in iso:
                agent = ''
                iso += '/download'
            else:
                agent = 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

            with open(f'tmp/{path}', 'wb') as f:
                c = Curl()
                c.setopt(c.URL, iso)
                c.setopt(c.USERAGENT, agent)
                c.setopt(c.FOLLOWLOCATION, True)
                c.setopt(c.AUTOREFERER,1)
                c.setopt(c.WRITEDATA, f)
                c.setopt(c.NOPROGRESS, False)
                c.setopt(c.XFERINFOFUNCTION, status)
                c.setopt(CAINFO, "/etc/ssl/certs/ca-certificates.crt")
                c.perform()
                effective = c.getinfo(c.EFFECTIVE_URL)
                if ('failedmirror' in effective) or (c.getinfo(c.RESPONSE_CODE) != 200):
                    print(f"Error downloading: {effective} => ", c.getinfo(c.HTTP_CODE))
                    return False
                c.close()
                return True

    def gnupg_verify (self, name):
        entry = iso_images[name]
        sign = entry.get('sign')
        sums = entry.get('sums')
        sum = entry.get('sum')
        key = entry.get('key')
        sf  = entry.get('sf')
        filename = entry["iso"].split('/')[-1]
        self.mark_unverified (name)
        if sign and not sums:
            if sign.startswith('https://'):
                if not self.download_file(sign):
                    print(f"*************************************************")
                    print(f"*ERROR - Missing signature => {name}")
                    print(f"*************************************************")
                    return
                sign = sign.split("/")[-1]
            else:
                with open(f'tmp/{filename}.sig', 'w') as w:
                    w.write(sign)
                sign = f'{filename}.sig'
            if key and not self.download_file(key):
                print(f"*************************************************")
                print(f"*ERROR - Missing key => {name}")
                print(f"*************************************************")
                return
            if key:
                ret = call([f'gpg --import tmp/{key.split("/")[-1]} 2>/tmp/SHAERR'], shell=True)
                if ret:
                    print (f'* ERROR importing key for {name}')
                    with open('/tmp/SHAERR') as io:
                        print(io.read())
                    return                
            ret = call([f'gpg --no-options --keyid-format long --verify tmp/{sign} isos/{filename} > /tmp/SHAERR'], shell=True)
            if ret:
                print (f'* ERROR verifying {name}')
                with open('/tmp/SHAERR') as io:
                    print(io.read())
            self.mark_verified (name)
            return
        if not sign or not sums:
            if not sf and not sum:
                print(f"*************************************************")
                print(f"*ERROR - Unable to verify, checksums unavailable: {name}")
                print(f"*************************************************")
                return

        if sign and sums:
            if not self.download_file (sign) or not self.download_file (sums):
                print(f"*************************************************")
                print(f"*ERROR - Missing checksums => {name}")
                print(f"*************************************************")
                return
            
            sign_file = sign.split('/')[-1]
            sum_file = sums.split('/')[-1]
            
            if name.startswith('fedora') or name.startswith('gentoo'):
                ret = call([f'gpgv --keyring tmp/{sign_file} tmp/{sum_file} 2>/tmp/SHAERR'], shell=True)
            else:
                ret = call([f'gpg --keyid-format long --verify tmp/{sign_file} tmp/{sum_file} 2>/tmp/SHAERR'], shell=True)
            if ret:
                print (f'* ERROR on {name} - SHASUMS corrupt')
                if ret:
                    with open('/tmp/SHAERR') as io:
                        print(io.read())
                return
        elif sf:
            if not self.download_file (sf):
                print(f"*************************************************")
                print(f"*ERROR - Missing checksums => {name}")
                print(f"*************************************************")
                return
            sum_file = sf.split('/')[-1]
        else:
            sum_file = None
           
        print ("Checking signature ...")
        path = Path(f'tmp/{filename}')
        if not path.exists():
            path = Path(f'isos/{filename}')
            if not path.exists():
                print(f"* File not available: {filename}")
                return
            
        wanted512 = self.checksum512(path)
        wanted256 = self.checksum256(path)
        wanted1 = self.checksum1(path)
            
        if sum:
            if sum in (wanted256, wanted512, wanted1):
                print(f'* Signature OK')
                self.mark_verified (name)
            else:
                print(f'* Signature BAD, found {sum}, wanted: {wanted1} / {wanted256} / {wanted512} (1)')
                self.mark_verified (name)
            return

        mode = 'text'
        with open (f'tmp/{sum_file}') as io:
            while True:
                line = io.readline()
                if not line: break
                line = line.strip('\n')
                if line.startswith('-----'):
                    mode = 'sig'
                if mode == 'text':
                    sign, file = [word for word in line.split(' ') if word]
                    
                    if file.strip("*") == filename:
                        if sign == wanted256 or sum == wanted512:
                            print(f'* Signature OK')
                            self.mark_verified (name)
                        else:
                            print(f'* Signature BAD, found {sign}')
                            print(f'* Wanted: {wanted256}, {wanted512} (2)')
                            self.mark_unverified (name)
                        return
                else:
                    if line.startswith('SHA256'):
                        sign = line.split('=')[-1].strip()
                        if sign in (wanted512, wanted256):
                            print(f'* Signature OK')
                            self.mark_verified (name)
                        else:
                            print(f'* Signature BAD, found {sign} wanted {wanted256}, {wanted512} (3)')
                            self.unmark_verified (name)
                        return
        print(f"* No such file listed: {filename}")

    def mark_verified (self, name):
        Path('verified').mkdir(exist_ok=True)
        with open(f'verified/{name}', 'w') as io:
            io.write(datetime.now().isoformat())

    def mark_unverified (self, name):
        Path('verified').mkdir(exist_ok=True)
        Path(f'verified/{name}').unlink(missing_ok=True)

    def checksum(self, path, hash_factory, chunk_num_blocks=16384):
        h = hash_factory()
        size = path.stat().st_size
        desc = path.as_posix().split('/')[-1].split('-')[0]
        with open(path.as_posix(),'rb') as f:
            with tqdm(total=size/(chunk_num_blocks*h.block_size)+1, desc=desc, bar_format="{l_bar}{bar}") as progress:
                while chunk := f.read(chunk_num_blocks*h.block_size): 
                    h.update(chunk)
                    progress.update()
        return h.hexdigest()

    def checksum1(self, path):
        return self.checksum(path, hashlib.sha1)

    def checksum256(self, path):
        return self.checksum(path, hashlib.sha256)

    def checksum512(self, path):
        return self.checksum(path, hashlib.sha512)

    def main (self):
        parser = ArgumentParser(
            prog="multiboot.py",
            description="USB Key Maintenance",
            epilog='Free Software for Linux from Mad Penguin Consulting Ltd')
        
        parser.add_argument("--list", action='store_true', help="List available ISO's")
        parser.add_argument("--update", action='store_true', help="Update software and signatures")
        parser.add_argument("--add", type=str, metavar="<iso>", help="The name of the ISO to add")
        parser.add_argument("--verify", type=str, metavar="<iso>|all", help="Verify the ISO's signatures")
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
        if not action:
            print ('No action specified, try adding --help')


if __name__ == '__main__':
    Multiboot().main()
    
