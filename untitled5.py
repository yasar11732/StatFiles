# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:30:42 2013

@author: muhammed
"""

from os import listdir
from pickle import load, dump
import logging
from random import sample

def load_file(name):
    with open(name) as dosya:
        return load(dosya)
        
def inbytes(size):
    position = 0
    while True:
        if not size[position].isdigit():
            break
        position += 1
    return int(size[:position]) * (1024 ** ["B","KB","MB"].index(size[position:]))


# normallist = load_file("normallist")

packages = load_file("working")
requires = []
"""for package in packages:
    
    try:
        p = load_file("packagemeta/%s" % package)
        requires.append((package,p["Requires Distributions"]))
    except Exception, e:
        pass"""