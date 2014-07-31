#!/usr/bin/python
#2014/7/28 this script will generate ceph daily workload report
import sys
import socket
import commands
import smtplib
from email.mime.text import MIMEText  
import time

def check_ceph_daily_workload(dict1):
	dict1=check_health(dict1)
	dict1=check_pool(dict1)
	return dict1

def check_health(dict1):
	print "<!--Checking ceph health-->"
     	cmd="ceph status"
     	dict1['cmd_ceph_health']=cmd
     	ret,output = commands.getstatusoutput(cmd)
     	output=output.replace('\n','<br>')
	dict1["ceph health"]=output
	return dict1

def check_pool(dict1):
	print "<!--Checking ceph pool status-->"
     	cmd="ceph osd dump|grep pool"
     	dict1['cmd_ceph_pool_status']=cmd
     	ret,output = commands.getstatusoutput(cmd)
     	output=output.replace('\n','<br>')
	dict1["ceph pool status"]=output
	return dict1

def run_command(dict1,key,command):
	print "<!--Checking "+key+"-->"
     	ret,output = commands.getstatusoutput(cmd)
     	output=output.replace('\n','<br>')
	dict1[key]=output
	return dict1

def get_html_body(dict1):
	date=time.strftime("%Y/%m/%d %H:%M:%S")
	hostname=socket.gethostname()
	list=['ceph health','ceph pool status']
	msg_head='''<html>
<head>
<title></title>
<style type="text/css">
table { 
	background:#F00
	border-width:2;
        border-style: solid;
} 

th {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #666666;
        background-color: #00FF00;
	text-align: left;
	font-size:20;
}

td {
	font-size:15px;
	text-align: left;
}

</style>
</head><body>'''
	msg="<H2>Ceph Daily Workload Report</H2>"
	msg=msg+"Hostname: "+hostname+"<br>"
	msg=msg+"Date: "+date+"<br><br>"

	#msg=msg+'<table class="gridtable"><tr class="heading">'
	msg=msg+'<table >\n'
	
	#for key in list:
	#	if dict1.has_key(key):
	#		msg=msg+"<b>"+key+"</b><br>"
	#		msg=msg+dict1[key]+"<br><br>"

	for key in list:
		if dict1.has_key(key):
			msg=msg+"<tr><th>"+key+"</th></tr>\n"+'<tr><td>'
			msg=msg+dict1[key]+"</td></tr>\n"

	msg=msg+'</tr></table>'
	msg_end='''</body></html>'''
	msg=msg_head+msg+msg_end
	print msg
	return msg

def output_report(dict1):
	date=time.strftime("%Y/%m/%d %H:%M:%S")
	hostname=socket.gethostname()

	sender = 'ceph-user@'+hostname
	receiver = 'andrew_yu@zeuscloud.cn'  
	subject = 'Ceph DWR '+date
	smtpserver = 'localhost'  
	username = 'root'  
	password = 'welcome1'  
	  
	#msg = MIMEText('<html><h1>hello world</h1></html>','html','utf-8')  
	msgbody=get_html_body(dict1)

	msg=MIMEText(msgbody,'html','utf-8')
	  
	msg['Subject'] = subject  
	  
	smtp = smtplib.SMTP()  
	smtp.connect('localhost')  
	#smtp.login(username, password)  
	smtp.sendmail(sender, receiver, msg.as_string())  
	smtp.quit()  

	#print "output:"+dict1["health"]
	all_list=['ceph_health']
	
	
	


if __name__=='__main__':
	dict1={}
     	dict1=check_ceph_daily_workload(dict1)
     	output_report(dict1)


