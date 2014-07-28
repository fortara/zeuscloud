#!/usr/bin/python
import sys
import commands

ssh="/usr/bin/ssh "

def check_remote(dict1):
	cmd=ssh+dict1['name']+" hostname"
	dict1['cmd_hostname']=cmd
	ret,output = commands.getstatusoutput(cmd)
	dict1['hostname']=output
	dict1=check_cpu(dict1)
	dict1=check_mem(dict1)
	dict1=check_disk(dict1)
	dict1=check_network(dict1)
	return dict1

def check_cpu(dict1):
	print "<!--Checking cpu statictic of "+dict1['name']+"-->"
	cmd=ssh+dict1['name']+" cat /proc/cpuinfo |grep \'model name\'|cut -f2 -d:|uniq -c"
	dict1['cmd_cpu_virtual']=cmd
	ret,output = commands.getstatusoutput(cmd)
	output=output.replace('\n','<br>')
	dict1['cpu_virtual']=output

	cmd=ssh+dict1['name']+" cat /proc/cpuinfo | grep 'physical id' | uniq -c"
	dict1['cmd_cpu_physical']=cmd
	ret,output = commands.getstatusoutput(cmd)
	output=output.replace('\n','<br>')
	dict1['cpu_physical']=output

	cmd=ssh+dict1['name']+" getconf LONG_BIT"
	dict1['cmd_cpu_bit']=cmd
	ret,output = commands.getstatusoutput(cmd)
	dict1['cpu_bit']=output
	
	return dict1

def check_mem(dict1):
	print "<!--Checking memory statictic of "+dict1['name']+"-->"
	cmd=ssh+dict1['name']+" free -g"
	dict1['cmd_mem_usage']=cmd
	ret,output = commands.getstatusoutput(cmd)
	output=output.replace('\n','<br>')
	dict1['mem_usage']=output

	#cmd=ssh+dict1['name']+" free -g|grep Mem|awk \'{print $4}\'"
	#ret,output = commands.getstatusoutput(cmd)
	#free_mem=int(output)-1
	##cmd=ssh+dict1['name']+" /opt/stability_test/bin/memtester "+str(free_mem)+"G 1"
	#cmd=ssh+dict1['name']+" /opt/stability_test/bin/memtester 10M 1"
	#dict1['cmd_mem_memtester']=cmd
	#ret,output = commands.getstatusoutput(cmd)
	#dict1['mem_mem_tester']=output
	
	return dict1
	
def check_disk(dict1):
	print "<!--Checking disk statictic of "+dict1['name']+"-->"
	cmd=ssh+dict1['name']+" df -h|egrep \"/vd|/sd\""
	dict1['cmd_disk_usage']=cmd
	ret,output = commands.getstatusoutput(cmd)
	output=output.replace('\n','<br>')
	dict1['disk_usage']=output

	#check disk io
	cmd=ssh+dict1['name']+" /opt/stability_test/bin/iozone -a -n 512m -g 1g -i 0 -i 1 -f /iozone.tmpfile -b /tmp/iozone.txt"
	dict1['cmd_disk_iozone']=cmd
	ret,output = commands.getstatusoutput(cmd)
	output=output.replace('\n','<br>')
	dict1['disk_iozone']=output

	#check bad blocks
	cmd=ssh+dict1['name']+" \"for i in \"`df -h|egrep \"/vd|/sd\"|awk '{print $1}'`\"; do echo checking badblocks of \$i;badblocks -s -v \$i ;done\""
	dict1['cmd_disk_badblocks']=cmd
	ret,output = commands.getstatusoutput(cmd)
	output=output.replace('\n','<br>')
	dict1['disk_badblocks']=output

	return dict1
	
def check_network(dict1):
	print "<!--Checking network statictic of "+dict1['name']+"-->"
	cmd=ssh+dict1['name']+" ip a"
	dict1['cmd_network']=cmd
	ret,output = commands.getstatusoutput(cmd)
	output=output.replace('\n','<br>')
	dict1['network']=output

	#check network bandwidth
	cmd="netperf -H "+dict1['name']+" -l 30"
	dict1['cmd_network_perf']=cmd
	ret,output = commands.getstatusoutput(cmd)
	output=output.replace('\n','<br>')
	dict1['network_perf']=output
	return dict1
	

def output_html(dict1):
	keys=dict1.keys()
	keys.sort()
	all_list=['cpu_virtual','cpu_physical','cpu_bit','mem_usage','mem_mem_tester','disk_usage','disk_iozone','disk_badblocks','network','network_perf']
	print "<b>"+"hostname"+"</b><br>"
	print dict1['hostname']+"<br><br>"
	for key in all_list:
		print "<b>"+key+"</b><br>"
		if dict1.has_key(key):
			print dict1[key]+"<br>"
	print "<br>"
	#for key in keys:
		#print key," => ",dict1[key]
		#print '%-20s => %-20s' % (key,dict1[key])

if __name__=='__main__':
	host=sys.argv[1]
	dict1={'name':host}
	dict1=check_remote(dict1)
	output_html(dict1)
