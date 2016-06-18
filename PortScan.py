#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author:lazynms

import optparse
import socket
from socket import *
from threading import Thread

screenLock=Semaphore(value=1)

def connScan(tgtHost,tgtPort):
	try:
		connSkt=socket(AF_INET,SOCK_STREAM)
		connSkt.connect((tgtHost,tgtPort))
		result=connSkt.recv(100)
		screenLock.acquire()
		print '[+] %d/tcp open'% tgtPort
		print '[+]  '+str(result)
	except Exception, e:
		screenLock.acquire()
		print '[-] %d/tcp closed'%tgtPort
	finally:
		screenLock.release()
		connSkt.close()
def portScan(tgtHost,tgtPorts):
	try:
		tgtIP=gethostbyname(tgtHost)
	except Exception, e:
		print "[-]  Cannot resolve '%s':Unkonw host"% tgtHost
		return
	try:
		tgtName=gethostbyaddr(tgtIP)
		print '\n[+] Scan Results for: '+tgtName[0]
	except Exception, e:
		print '\n[+] Scan Results for: '+tgtIP

	setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		t=Thread(target=connScan,args=(tgtHost,int(tgtPort)))
		t.start()

def main():
	parser=optparse.OptionParser("usage %prog "+"-H <target host> -p <target port>")
	parser.add_option("-H",dest='tgtHost',type='string',help='specify target host' )
	parser.add_option("-p",dest="tgtPort",type='string',help="specify target port")
	(options,args)=parser.parse_args()
	print options
	tgtHost=options.tgtHost
	tgtPorts=str(options.tgtPort).split(',')
	if (tgtHost == None)|(tgtPorts[0] == None):
		print "[-] You must specify a target host and port[s]..."
		exit(0)
	portScan(tgtHost,tgtPorts)

if __name__=="__main__":
	main()

