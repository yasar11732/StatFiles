# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 02:27:52 2013

@author: muhammed
"""


from pickle import load, dump
from BeautifulSoup import BeautifulSoup
from urllib import urlopen, urlretrieve, quote
from threading import Thread
from Queue import Queue

from time import sleep


def load_file(name):
    with open(name) as dosya:
        return load(dosya)

def save_file(name):
    with open(name,"w") as dosya:
        return dump(globals()[name],dosya )

with open("packageindex.html") as dosya:
    s = BeautifulSoup(dosya)
    
table = s("table", attrs={'class':'list'})[0]

packages = {}
for row in table("tr"):
    if row.td:
        try:
            _, _, base, version = row.td.a.get('href').split("/")
            try:
                packages[base].append(version)
            except KeyError:
                packages[base] = [version]
        except AttributeError:
            pass
        
save_file("packages")