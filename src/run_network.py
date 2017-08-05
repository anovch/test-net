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
	if (not os.path.isfile('./run_qemu')):
		print 'Error !!! Config file "./run_qemu" not found '
		exit(1)
	
	subprocess.call("./run_qemu > output.log 2>&1 &", shell=True)
	print "Run instance: ", name

 	
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
	