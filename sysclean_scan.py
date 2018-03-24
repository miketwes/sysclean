#!/usr/bin/env python3.4

## Sysclean
## Copyright (C) 2013 miketwes mt.kongtong@gmail.com
## https://github.com/miketwes/sysclean
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.


import subprocess
import math

def convertSize(size):
	size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size,1024)))
	p = math.pow(1024,i)
	s = round(size/p,2)
	if (s > 0):
		return '%s %s' % (s,size_name[i])
	else:
		return '0B'

def runcmd(cmd):

	p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE , stderr=subprocess.PIPE)
	stdout, stderr = p.communicate()
	return (stdout, stderr,p.returncode)

def getsize():
	
	usrn = subprocess.check_output('env | grep PWD', shell=True).splitlines()[0].split(b'=')[1].decode()       
	total_size = 0
	sizelist = []
	
	c0 = [	
			["free | grep Mem: | awk '{print $6+$7}'","buffers_cache"],
			["deborphan -z | awk '{ sum+=$1} END {print sum}'", 'deborphan'],
			['du -s /var/log'],
			['du -s /var/tmp'],
			['du -s /tmp'],
			['du -s /var/cache/apt/archives'],
			['du -s ' + usrn + '/.bash_history'],
			['du -s /root/.bash_history'],
			["du -s " + usrn + "/.cache/mozilla/firefox/*.default/*.sqlite | awk '{ sum+=$1} END {print sum}'",'firefox_cache'],				
			['du -s ' + usrn + '/.mozilla/firefox/*default/sessionstore.js']						
		 ]


	c1 = [
			'swapoff -a;swapon -a;echo 3 > /proc/sys/vm/drop_caches',
			'aptitude -y purge $(deborphan)',
			"""rm -f /var/log/*.gz;rm -f /var/log/*/*.gz;find /var/log -type f -regex ".*\.[0-9]$" -delete;loglist=`find /var/log -type f`;for i in $loglist;do > $i;done;""",
			'rm -rf /var/tmp/*',	
			'rm -rf /tmp/*',	
			"""apt-get autoclean;apt-get clean;apt-get -y autoremove;""",
			'> ' + usrn + '/.bash_history',
			'> /root/.bash_history',		        
			'rm -r ' + usrn + '/.cache/mozilla/firefox/*.default/*',
			'rm -r ' + usrn + '/.mozilla/firefox/*default/sessionstore.js'
		 ]	
		 
	cmdlist = []	
	
	cmd = 'sudo find /etc/ -name "*.dpkg-dist" -o -name "*.dpkg-new" -o -name "*.dpkg-old" -o -name "*.ucf-dist" -o -name "*.ucf-new" -o -name "*.ucf-old"'
	etc_trash = subprocess.check_output(cmd, shell=True).splitlines()
	etc_trash = [x.decode() for x in etc_trash]	
	if len(etc_trash) > 0:
		for x in etc_trash:
			c0.append('du -s '+ x)
			c1.append('rm -r '+ x)

	i = 0
	for cmd in c0:
		
		if  len(cmd) == 1:			
			cmdtext = cmd[0].split(' ')[-1]	
			cmd[0] += "  | awk '{print $1}'"
		else:
			cmdtext = cmd[1]

		stdout, stderr,exitCode = runcmd(cmd[0])
		
		if exitCode == 0:
			s1 = stdout.splitlines()
			if len(s1) > 0 and s1[0] != b'':				
				s = int(s1[0].decode())
				if s > 0:
					total_size += s
					sizelist.append(cmdtext + ': ' + convertSize(s))
					cmdlist.append(c1[i])
		i += 1				    
				
	cmd = 'dpkg --get-selections | grep deinstall | cut -f1'	
	stdout, stderr,exitCode = runcmd(cmd)
	if stdout != b'':
		cmdlist.append("dpkg --purge `"+ cmd + "`")
	cmd = "df --total | grep total | awk '{print $4}'"
	stdout, stderr,exitCode = runcmd(cmd)
	if stdout != b'':	
			stdout = int(stdout.splitlines()[0].decode())
	sizelist.append("")
	
	if total_size > 0:
		sizelist.append('total_size: ' + convertSize(total_size)) 
	else:
		sizelist.append('total_size: 0') 
	
	if stdout > 0:
		sizelist.append('available disk space: ' + convertSize(stdout)) 
	else:
		sizelist.append('available disk space: 0') 

	return (sizelist, cmdlist, total_size,stdout)


def clean_up(cmd):
	
	stdout, stderr,exitCode = runcmd(cmd)
	if exitCode == 0:
		return cmd + " success \n"
	else:
		return cmd + " failed " + stderr.decode() + "\n"
