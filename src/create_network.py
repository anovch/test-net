#!/usr/bin/python
from subprocess import Popen, PIPE
import shutil
import os
import sys
import json
import subprocess
import time
			
qemu = 'qemu-system-x86_64 -hda ./rootfs  -kernel ./bzImage -append "console=ttyS0 root=/dev/hda initrd=/initrd" -nographic'

def WriteToFile(fiename, data):
	text_file = open(fiename, "w")
	text_file.write(data)
	text_file.close()
	os.chmod(fiename, 755)	
	
'''
	Copy and create instance of the quemu.  
'''
def CreateInstance(name, data):
	dirname = "../"+name;

	if ((not os.path.isfile('rootfs')) or (not os.path.isfile('bzImage'))):
		print "Error !!! rootfs or bzImage not found"
		exit(1)

	print "Instance dir: ", dirname
	if (os.path.exists(dirname)):
		shutil.rmtree(dirname)
	
	os.mkdir(dirname)
	os.mkdir(dirname+"/mnt")
	
	#copy file
	shutil.copy2('rootfs', dirname+'/rootfs')	
	shutil.copy2('bzImage', dirname+'/bzImage')	
	
	run_qemu = '#!/bin/sh\n';
	run_qemu_interfaces = ''
	index = 1
	for interfaces in sorted(data[name]):
		mac = data[name][interfaces]['mac']
		ip = ''
		netmask = ''
		if 'ip' in data[name][interfaces]:
			ip = data[name][interfaces]['ip']
		if 'netmask' in data[name][interfaces]:
			netmask = data[name][interfaces]['netmask']
		switch = data[name][interfaces]['switch']
		print 'mac={} ip={}/{} switch={}'.format(mac,ip,netmask,switch)
		run_qemu += 'macaddres{}={}\n'.format(index,mac)	
		run_qemu_interfaces +=' -device e1000,netdev=net{},mac=$macaddres{} -netdev tap,id=net{},script=./qemu-ifup{}'.format(index,index,index,index)
		# create ifup scripts --------------
		script_name = 'qemu-ifup{}'.format(index)
		script_data = ''
		with open('ifup', 'r') as myfile:
			script_data=myfile.read().replace('{switch}', switch)
		WriteToFile(dirname+'/'+script_name,script_data)
		index += 1	
	
	run_qemu += qemu + run_qemu_interfaces	
	WriteToFile(dirname+'/run_qemu',run_qemu)		

	

		
network_template="""
auto {interface}
iface {interface} inet static 
	{ip}
	{netmask}
	{network}
"""
	
def SetNotworkConfig(name, data, process):
	out	= "\\nauto lo\\niface lo inet loopback\\n"
	for interfaces in sorted(data[name]):
		mac = data[name][interfaces]['mac']
		ip = ''
		netmask = ''
		network = ''
		network_manager = ''
		if 'ip' in data[name][interfaces]:
			ip = data[name][interfaces]['ip']
		if 'netmask' in data[name][interfaces]:
			netmask = data[name][interfaces]['netmask']
		if 'network' in data[name][interfaces]:
			network = data[name][interfaces]['network']
		if 'network_manager' in data[name][interfaces]:
			network_manager = data[name][interfaces]['network_manager']
		
		if (len(ip)==0):
			continue
		network_conf = network_template
		network_conf = network_conf.replace("{interface}", interfaces)
		network_conf = network_conf.replace("{ip}", "address "+ip)		
		network_conf = network_conf.replace("{netmask}", "netmask "+netmask)				
		if (len(network)==0):
			network_conf = network_conf.replace("{network}", "")				
		else:
			network_conf = network_conf.replace("{network}", "network "+network)						
		if (len(network_manager)!=0):
			command = "echo \""+network_manager+"\" >> /etc/init.d/rc\n\r"
			process.stdin.write(command);
			
		network_conf = network_conf.replace("\n", "\\n")				
		out += network_conf
	
	command = "echo -e \""+out+"\" > /etc/network/interfaces\n\r"
	#print command
	process.stdin.write(command);

	command = "echo \""+name+"\" > /etc/hostname\n\r"
	process.stdin.write(command);
		
'''
	Run instance of the quemu.  
	Setup hostname and menagement IP for eth0 interface
'''
#def RunInstance(name, data):
#	SetNotworkConfig(name, data, '')
	
def RunInstance(name, data):
	print "Run instance: ", name
	dirname = "../"+name;	
	os.chdir(dirname)
	if (not os.path.isfile('./run_qemu')):
		print 'Error !!! Config file "./run_qemu" not found '
		exit(1)
	
	
	load_completed_phrase='Poky (Yocto Project Reference Distro)'
	process = Popen(['sudo','./run_qemu'],stdout=PIPE,stdin=PIPE,close_fds=True)
	
	while True:
		next_line = process.stdout.readline()
		if not next_line:
			break
		sys.stdout.write(next_line)
		sys.stdout.flush()
		
		if load_completed_phrase in next_line:
			time.sleep(1)
			process.stdin.write('root\n\r');
			time.sleep(0.5)
			SetNotworkConfig(name, data, process)
			time.sleep(0.5)
			process.stdin.write('halt\n\r');
		
	print "End run instance: ", name
	
 	
'''
	main  
'''
filenameconfig = 'conf.json'
if (len(sys.argv)>=2):
	filenameconfig = sys.argv[1]

print '#############################################################'
print 'Builder qemu instance ver 1'
print 'Config file :', filenameconfig

if (not os.path.isfile(filenameconfig)):
	print 'Error !!! Config file "{}" not found'.format(filenameconfig)
	exit(1)
		
with open(filenameconfig) as json_data_file:
    data = json.load(json_data_file)

for hosts in data:
    CreateInstance(hosts, data)

for hosts in data:
    RunInstance(hosts, data)
	