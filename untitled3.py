# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 14:43:06 2013

@author: muhammed
"""

import multiprocessing
from pickle import load, dump
from untitled4 import Task
import logging
from traceback import print_exc

class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, brokens):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.brokens = brokens

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            try:
                next_task()
            except Exception, e:
                self.brokens.put((str(next_task),e))
            self.task_queue.task_done()
        return




def load_file(name):
    with open(name) as dosya:
        return load(dosya)
    
        
def save_file(name):
    with open(name,"w") as dosya:
        return dump(globals()[name],dosya )  
            

if __name__ == '__main__':
    from time import sleep
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    brokens = multiprocessing.JoinableQueue()
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print 'Creating %d consumers' % num_consumers
    consumers = [ Consumer(tasks, brokens)
                  for i in xrange(num_consumers) ]
    for w in consumers:
        w.daemon = True
        w.start()
    
    # Enqueue jobs
    #packages = load_file("broken_downloads")
    # print packages

    from os import listdir
    for fname in listdir("cache"):
        tasks.put(Task(fname))
    
    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)
        
    while True:
        a = tasks.qsize()
        print "remainin:",a,"broken", brokens.qsize()
        if a < 10:
            break
        sleep(5)
    # Wait for all of the tasks to finish
    tasks.join()
    brk = []
    
    while not brokens.empty():
        brk.append(brokens.get())
    
    print brk
    save_file("brk")