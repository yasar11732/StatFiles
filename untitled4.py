# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 14:59:06 2013

@author: muhammed
"""

from BeautifulSoup import BeautifulSoup as soup
import logging
from pickle import dump

class Task(object):
    def __init__(self, package):
        self.package = package
    
    def __call__(self):
        meta = {}
        meta["packagename"] = self.package
        
        with open("cache/%s" % self.package) as dosya:
            s = soup(dosya)

        section = s("div",attrs={'class':'section'})[0]

        try:
            table = section("table", attrs={'class':'list','style':'margin-bottom: 10px;'})[0]
            
            row = table("tr")[1]
            cells = row("td")
            meta["filename"] = cells[0].span.a.string.strip()
            meta["filetype"] = cells[1].string.strip()
            meta["pyversion"] = cells[2].string.strip()
            meta["uploaded"] = cells[3].string.strip()
            meta["size"] = cells[4].string.strip()
        except IndexError:
            pass
        

        downloads, meta_section = section("ul", attrs={'class':'nodot'})[0:2]

        
        listitems = downloads("li")
        meta["daily"] = listitems[1].span.string
        meta["weekly"] = listitems[2].span.string
        meta["monthly"] = listitems[3].span.string
        
        for li in meta_section("li", recursive=False):
            cnts = []
            key = li.strong.string
            if not key:
                continue
            key = str(key)
            
            if li.span:
                value = li.span.string
            elif li.a:
                value = li.a.string
            elif li.ul:
                value = li.ul.string
            else:
                value = li.contents[-1]
            
            meta[key] = value
            
        for k,v in meta.items():
            meta[k] = unicode(v).strip()

        with open("packagemeta-3/%s" % self.package,"w") as dosya:
            dump(meta, dosya)
        
        
    
    def __str__(self):
        return 'Task: %s' % (self.package)