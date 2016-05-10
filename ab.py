#! /usr/bin/env python
#coding: utf-8
'''
这个部分主要是来获得参数，并执行测试
'''
__author__ = 'huhao'
VERSION = '0.0.1'
import sys
import getopt
import gevent
from gevent import monkey
monkey.patch_all()
from getresult import *
class AB(object):
    def __init__(self):
        self.url = ''
        self.counts = 1
        self.current = 1
        self.postdata = ''
        self.proxy = ''
    def ab(self):
        opt,argv = getopt.getopt(sys.argv[1:],'hvn:c:p:P:')
        if len(argv) > 0:
            self.url = argv[0]
        for key,value in opt:
            if key == '-v':
                print 'Version:',VERSION
            if key == '-n':
                try:
                    self.counts = int(value)
                except:
                    print 'please inpute requests number'
            if key == '-c':
                try:
                    self.current = int(value)
                except:
                    print 'please inpute concurrency number'
            if key == '-p':
                try:
                    self.postdata = value
                except:
                    print 'please inpute post data:'
            if key == '-P':
                try:
                    self.proxy = value
                except:
                    print 'please inpute proxy:'

            if key == '-h':
                print("Options are:")
                print("""
    -n requests     Number of requests to perform
    -c concurrency  Number of multiple requests at a time
    -p post         post data
    -P              proxy
    -v              Print version number
    -h              Display usage information
    """)
a = AB()
a.ab()
r = getResult()
r.url = a.url
r.count = a.counts
r.current = a.current
if r.url != '':
    temp = []
    if a.postdata != '':
        r.post_data = a.postdata
    if a.proxy != '':
        r.proxy = a.proxy
    for i in xrange(r.current):
        temp.append(gevent.spawn(r.counts(r.count)))
    gevent.joinall(temp)
    r.out_print()
    r.statistics()
