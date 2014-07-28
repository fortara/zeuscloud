#!/bin/bash
host=`hostname`
echo "STABILITY TESTING"
echo "	hostname: $host"
echo
echo "CPU Testing:"
vcpu_info=`cat /proc/cpuinfo |grep 'model name'|cut -f2 -d:|uniq -c`
echo "	VIRTUAL CPU NUM:"
echo "	$vcpu_info"
echo
pcpu_info=`cat /proc/cpuinfo | grep 'physical id' | uniq -c`
echo "	PHYSICAL CPU NUM:"
echo "	$pcpu_info"
bit=`getconf LONG_BIT`
echo "	CPU Level:"
echo "	$bit"
echo
mem=`free -g`
echo "MEM Testing:"
echo "$mem"

