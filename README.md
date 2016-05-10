类似APACHE BENCHMARK 的python实现 ab


Apache Benchmark 的python模仿，实现功能如下：
  例如： python ab.py -n 10 -c 3 www.baidu.com
  参数：
  
 -n ： 发送请求的数量
 -c ： 并发的数量
 -v :  版本信息
 -h :  帮助信息
 -p ： post的数据
 -P :  代理设置

实现思路:
1. 使用pycurl获得测试站点的信息
2. 使用gevent实现并发

实现过程:
1.分为两个部分，第一部分是脚本的参数设置，并执行测试ab.py
2.第二部分为获取想要的数据，和输出打印getresult.py

编写环境

系统 Centos 7, python -V : Python 2.7.10 依赖包 pycurl ,gevent
