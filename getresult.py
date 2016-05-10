#! /usr/bin/env python
#coding: utf-8
'''
这个部分主要是获得测试web的一些参数
'''
import pycurl
import StringIO
import re
import gevent
from gevent import monkey
monkey.patch_all()
class getResult(object):
    def __init__(self):
        '''
        初始化一些参数
        :return:
        '''
        self.url = ''
        self.method = "GET"
        self.b = StringIO.StringIO()
        self.getheader = StringIO.StringIO()
        self.post_data = None
        self.proxy = None
        self.current = 1
        self.count = 1
        self.info = []
        self.sumtime = 0
    def result_parse(self):
        '''
        获得所需要的web参数
        :return:
        '''
        result = {}
        temp = ''
        c = pycurl.Curl()
        c.setopt(c.URL,self.url)
        c.setopt(c.WRITEFUNCTION,self.b.write)
        c.setopt(pycurl.HEADERFUNCTION, self.getheader.write)
        if self.method == 'POST':
             c.setopt(c.POSTFIELDS,self.post_data)
        if self.proxy != None:
             c.setopt(c.PROXY,self.proxy)
        c.setopt(c.MAXREDIRS,5)
        c.setopt(c.CONNECTTIMEOUT,60)
        c.perform()
        body = self.getheader.getvalue()
        pattern = re.compile(r'Server')
        text = body.split('\n')
        for line in text:
            match = pattern.search(line)
            if match:
                temp = line.split(':')[1].strip()
        result['Server Software'] = temp
        result['Server Hostname'] = c.getinfo(pycurl.EFFECTIVE_URL).split('//')[1].split('/')[0]
        result['Server IP'] = c.getinfo(pycurl.PRIMARY_IP)
        result['Server Port'] = ""
        if c.getinfo(pycurl.EFFECTIVE_URL).split('//')[0].capitalize() == 'Http:':
            result['Server Port'] = 80
        if c.getinfo(pycurl.EFFECTIVE_URL).split('//')[0] == 'Https:':
            result['Server Port'] = 443
        result['Document Path'] = '/'+c.getinfo(pycurl.EFFECTIVE_URL).split('//')[1].split('/')[1]
        result['Total transferred'] = c.getinfo(pycurl.SIZE_DOWNLOAD)
        result['HTML transferred'] = c.getinfo(pycurl.SIZE_DOWNLOAD)-c.getinfo(pycurl.HEADER_SIZE)
        result['Document Length'] = c.getinfo(pycurl.SIZE_DOWNLOAD)-c.getinfo(pycurl.HEADER_SIZE)
        result['Time taken for tests']= c.getinfo(pycurl.TOTAL_TIME)
        result['Name lookup time']= c.getinfo(pycurl.NAMELOOKUP_TIME)
        result['Waiting']= c.getinfo(pycurl.STARTTRANSFER_TIME)
        result['Connect']= c.getinfo(pycurl.CONNECT_TIME)
        result['Http Code']= c.getinfo(pycurl.HTTP_CODE)
        return result
    def counts(self,count):
        '''
        执行多次请求
        :return:
        '''
        n = 0
        count = self.count
        for i in xrange(count):
            temp = []
            temp = self.result_parse()
            self.info.append(temp)
        for i in xrange(count):
            if self.info[i]['Http Code'] == 200:
                n = n+1
        print("Completed %d requests" % n)
    def statistics(self):
        '''
        统计获得的参数
        :return:
        '''
        t = []
        w = []
        c = []
        n = 0
        for i in xrange(self.count):
            t.append(self.info[i]['Time taken for tests'])
            w.append(self.info[i]['Waiting'])
            c.append(self.info[i]['Connect'])
            if self.info[i]['Http Code'] == 200:
                n = n+1
        t.sort()
        w.sort()
        c.sort()
        t_mean = sum(t)/self.count
        w_mean = sum(w)/self.count
        c_mean = sum(c)/self.count
        print "Complete requests:      ",n
        print "Failed requests:        ",self.count-n
        print "Requests per second:    ",int(1/t_mean)
        print "Time per request:       ",t_mean
        print ""
        print"               min  mean median   max"
        print"Connect:      ",c[0], c_mean, c[self.count/2], c[self.count-1]
        print "Waiting:     ", w[0], w_mean, w[self.count/2], w[self.count-1]
        print "Total:       ",t[0], t_mean,t[self.count/2],t[self.count-1]
        print "Time taken for tests:   ",sum(t)
    def out_print(self):
        '''
        打印输出
        :return:
        '''
        print ""
        print "Server Software:        ",self.result_parse()['Server Software']
        print "Server Hostname:        ",self.result_parse()['Server Hostname']
        print "Server Port:            ",self.result_parse()['Server Port']
        print "Document Path:          ",self.result_parse()['Document Path']
        print "Document Length:        ",self.result_parse()['Document Length']
        print "Concurrency Level:      ",self.current
        print "HTML transferred:       ",self.result_parse()['HTML transferred']
        print "Transfer rate:          ",self.result_parse()['Total transferred']/self.result_parse()['Time taken for tests']
        print "Connection Times:       ",self.result_parse()['Connect']
