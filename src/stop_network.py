#!/usr/bin/python
from subprocess import Popen, PIPE
import shutil
import os
import sys
import json
import subprocess
import time
			
	
def RunInstance(name, data):

	dirname = "../"+name;	
	os.chdir(dirname)

	for interfaces in sorted(data[name]):
		ip = ''
		if 'ip' in data[name][interfaces]:
			ip = data[name][interfaces]['ip'] 	
	
		if ((len(ip)!=0) and (interfaces == 'eth0')): 
			command = 'umount ./mnt/'
			subprocess.call(command, shell=True)
			command = "ssh root@" + ip + " 'halt'"
			subprocess.call(command, shell=True)
			print "Umount fs : ", name, ip

 	
'''
	main  
'''
filenameconfig = 'conf.json'
if (len(sys.argv)>=2):
	filenameconfig = sys.argv[1]

print '#############################################################'
print 'Runner qemu instance ver 1'
print 'Config file :', filenameconfig

if (not os.path.isfile(filenameconfig)):
	print 'Error !!! Config file "{}" not found'.format(filenameconfig)
	exit(1)
		
with open(filenameconfig) as json_data_file:
    data = json.load(json_data_file)


for hosts in data:
    RunInstance(hosts, data)

#subprocess.call('pkill -9 qemu-system-x86 ', shell=True)