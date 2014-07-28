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
	return dict1

def check_health(dict1):
	print "<!--Checking ceph health-->"
     	cmd="ceph health"
     	dict1['cmd_ceph_health']=cmd
     	ret,output = commands.getstatusoutput(cmd)
     	output=output.replace('\n','<br>')
	dict1["ceph_health"]=output
	return dict1

def check_rados(dict1):

	return dict1

def get_html_body(dict1):
	date=time.strftime("%Y/%m/%d %H:%M:%S")
	hostname=socket.gethostname()
	msg_head='''<html>
<head>
<title></title>
</head><body>'''
	msg="<H1>Ceph Daily Workload Report</H1>"
	msg=msg+"Hostname: "+hostname+"<br>"
	msg=msg+"Date: "+date+"<br>"

	
	list=['ceph_health']
	for key in list:
		msg=msg+"<b>"+key+"</b><br>"
		msg=msg+dict1[key]+"<br>"

	msg_end='''</body></html>'''
	msg=msg_head+msg+msg_end
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


