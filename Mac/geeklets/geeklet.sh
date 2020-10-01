#!/bin/bash

# Make sure you change the following variable 
# to match the network interface you would like to monitor
nic=en0

echo "CPU information:"
sysctl -n machdep.cpu.brand_string

# Find current bandwith in each pipe
myvar1=`netstat -bI ${nic} | awk "/${nic}/"'{print $7;exit}'`
myvar3=`netstat -bI ${nic} | awk "/${nic}/"'{print $10;exit}'`

# Find current bandwith in each pipe after a second.
myvar2=`netstat -bI ${nic} | awk "/${nic}/"'{print $7;exit}'`
myvar4=`netstat -bI ${nic} | awk "/${nic}/"'{print $10;exit}'`

# Find the difference between each pipe after 1 second.
subin=$(($myvar2 - $myvar1))
subout=$(($myvar4 - $myvar3))


# Convert the bytes to kilobytes
kbin=`echo "scale=2; $subin/1024;" | bc`
kbout=`echo "scale=2; $subout/1024;" | bc`

# Current CPU usage
cpu="`ps -A -o %cpu | awk '{s+=$1} END {print s "%"}'`"

# Current Memory Usage
hwmemsize=$(sysctl -n hw.memsize)
# 1024**3 = GB
ramsize=$(expr $hwmemsize / $((1024**3)))

mem="`ps -A -o %mem | awk '{s+=$1} END {print s "%"}'`"

echo "CPU Usage: $cpu"
echo "CPU temperature: `sysctl -n machdep.xcpm.cpu_thermal_level` C"
echo "System Memory: ${ramsize} GB"
echo "RAM Usage: $mem"
echo

echo Network Information:

# Current IP Address
# Current Network Traffic
echo "IP address:"
echo "`ifconfig ${nic} | grep inet`"
echo "Upload: $kbout KB/s"
echo "Download: $kbin KB/s"
# Current uptime
echo Uptime: `uptime | sed -E "s/^[0-9]+:[0-9]+[[:space:]]+up //" | sed -E "s/, [0-9] users.*//"`
echo

echo "SSD information:"
echo "`diskutil info disk0s2 | grep Total`"
echo "`diskutil info disk0s2 | grep Used`"
echo "`diskutil info disk0s2 | grep Available`"
