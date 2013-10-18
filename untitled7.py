# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 03:01:15 2013

@author: muhammed
"""
from os import listdir
from pickle import load, dump
import logging
from random import sample
from os.path import basename

def load_file_global(name):
    print "loading", name, "as", basename(name),"...",
    if basename(name) not in globals():
        with open(name) as dosya:
            globals()[basename(name)] = load(dosya)
    else:
        print "already loaded..",
    print "done"

def load_file_return(name):
    with open(name) as dosya:
        return load(dosya)
        
def save_file(name):
    print "saving", name,"..."
    with open(name,"w") as dosya:
        return dump(globals()[name],dosya )
    print "done"


def inbytes(size):
    position = 0
    while True:
        if not size[position].isdigit():
            break
        position += 1
    return int(size[:position]) * (1024 ** ["B","KB","MB"].index(size[position:]))

load_file_global("file_requires_score")
load_file_global("file_size")

file_size.sort(key= lambda x: x[1], reverse=True)
save_file("file_size")

def delparen(s):
    start = 0
    pos = 0
    parenlevel = 0
    chars = []
    while True:
        try:
            current = s[pos]
        except IndexError:
            break
        pos += 1
        if current == "(":
            parenlevel += 1
        elif current == ")":
            parenlevel -= 1
        elif parenlevel == 0:
            chars.append(current)
            
    if parenlevel:
        raise ValueError("unclosed paren in %s" % s)
    
    return "".join(chars)


def get_list_from_string(s):
    
    s = delparen(s)    
    packs = s.split(",")
    packs = [x.strip() for x in packs]
    return packs

def give_point_recursive(to, visited=set()):
    print "give score to", to   
    
    try:
        all_in_one[to.lower()]['requires_score'] += 1
    except KeyError:
        if to.lower() in all_in_one:
            all_in_one[to.lower()]['requires_score'] = 1
        else:
            all_in_one[to.lower()] = {}
            all_in_one[to.lower()]['requires_score'] = 1
    
    
    try:
        req_string = file_requires[to]
    except KeyError:
        return

    visited.add(to)
    for p in get_list_from_string(req_string):
        if p not in visited:
            give_point_recursive(p, visited)

# save_file("all_in_one")"""