# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 01:27:08 2013

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

urltemplate = "https://pypi.python.org/pypi/%s/%s"

still_broken = []
def worker(que, sbroken):
    print "worker starting"
    while True:
        pack, version = que.get()
        if pack is None and version is None:
            que.task_done()
            break
        try:
            urlretrieve(urltemplate % (pack, version), "cache/%s" % pack)
        except:
            print urltemplate % (quote(pack), quote(version))
            sbroken.put((pack, version))
        que.task_done()
    print "worker exiting"

if __name__ == '__main__':
    # Establish communication queues
    tasks = Queue()
    sbroken = Queue()
    
    # Start consumers
    num_consumers = 250
    print 'Creating %d consumers' % num_consumers
    consumers = [ Thread(target=worker, args=(tasks,sbroken)) for _ in xrange(num_consumers)]
    for w in consumers:
        w.daemon = True
        w.start()
    
    # Enqueue jobs
    packages = load_file("broken_downloads")
    # print packages
    for pack, version in packages:
        if pack == "aux":
            continue
        tasks.put((pack,version))
    
    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put((None, None))

    while True:
        a = tasks.qsize()
        print "Task remaining", a,"broken:", sbroken.qsize()
        sleep(3)
        if a < 10:
            break
    tasks.join()
    
    while not sbroken.empty():
        still_broken.append(sbroken.get())
        
    save_file("still_broken")
    print still_broken
    print len(still_broken), "still broken downloads"
        