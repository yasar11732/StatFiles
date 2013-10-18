# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 00:59:09 2013

@author: muhammed
"""

from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from pickle import dump, load

def load_file(name):
    with open(name) as dosya:
        globals()[name]= load(dosya)
        
def save_file(name):
    with open(name,"w") as dosya:
        dump(globals()[name], dosya)

from os import stat

load_file("packages")
broken_downloads = []

for pack, versions in packages.items():
    try:
        if os.stat("packagemeta/%s" % pack).st_size == 0:
            broken_downloads.append((pack,sorted(versions)[-1]))
    except:
        broken_downloads.append((pack,sorted(versions)[-1]))
        
save_file("broken_downloads")
print broken_downloads
print len(broken_downloads)