# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:10:45 2013

@author: muhammed
"""
from urllib import urlretrieve, quote
from pickle import load
from Queue import Queue
from threading import Thread
from os import stat

def load_file(name):
    with open(name) as dosya:
        globals()[name]= load(dosya)

def retrieve(que):
    while True:
        site = que.get()
        urlretrieve("https://pypi.python.org/pypi/%s" % quote(site), "cache/%s" % site)
        que.task_done()

load_file("packages")

for pack in packages:
    try:
        if os.stat("cache/%s" % pack).st_size == 0:
            print pack
    except WindowsError:
        print pack
