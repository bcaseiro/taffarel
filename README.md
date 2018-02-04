# 
# A video demonstration showing taffarel.py in action is available at - https://www.youtube.com/watch?v=1_5Pg2ghQOI
#
# ###########################
# FAQ:
#
# 1) What it does?
# It will identify two type of Privileged Users on Linux/Unix systems. Root Users (ID 0) and Users who have some sort of sudoer's privilege. The results will be printed on the screen and also exported to a .XLS # file called PrivilegedAccounts.xls on the /tmp/ directory.
#
# 2) Why this name "taffarel"? 
# The insipiration was a goalkeeper - https://www.youtube.com/watch?v=HlCGkxgQ56c
# 
# 3) Why I wrote this tool?
# The goal is to assist sysadmins and IT auditors to identify privileged accounts in the environment so they can make sure that those accounts are protected properly.
#
# 4) Can I modify this tool?
# Sure, it's a free tool and it was coded in python to make things easier!
#
# 5) How to install it?
# Just download the tool (taffarel.py) and copy it to a folder in your Linux system. I developed this tool using the Kali Linux, since it included already all python libraries that I needed.
# I developed this script using the version: Linux kali 4.13.0-kali1-amd64 #1 SMP Debian 4.13.10-1kali2 (2017-11-08) x86_64 GNU/Linux
#
# 6) How do I run this tool?
# Type: "python taffarel.py -h" for more information.
#
# Usage..: 
# python taffarel.py 192.168.142.20 
# python taffarel.py server01
# python taffarel.py server01.btlab.ca
# python taffarel.py 192.168.142.0/24
# Author: Bruno Caseiro (bacaseiro@gmail.com) 
# #####################################################
# 
# 
# 
# This is a typical result or output:
 
# ----------------------------------------------------------------------------------------------------
# Finding Privileged Users on the network: 192.168.142.42/29 -------------       Please wait     
# ----------------------------------------------------------------------------------------------------
# 
# Host is not accessible: 192.168.142.41
# Host 192.168.142.42 responded successfully to the ping command
# Host: 192.168.142.42 - Sudoer User: root - Permission: ALL = (ALL)NOPASSWD: ALL  # Linux Built-In account
# Host: 192.168.142.42 - Sudoer User: svclinux - Permission: ALL = (ALL)NOPASSWD: ALL  
# Host: 192.168.142.42 - Sudoer User: %sudoersfullaccess - Permission: ALL = (ALL)NOPASSWD: ALL 
# Host: 192.168.142.42 - Sudoer User: german - Permission: ubuntu01.btlab.ca = (ALL)NOPASSWD: ALL
# Host: 192.168.142.42 - Sudoer User: bruno - Permission: linuxsrv09 = (ALL)NOPASSWD: ALL
# Host: 192.168.142.42 - Root User: root
# Host is not accessible: 192.168.142.43
# Host 192.168.142.44 responded successfully to the ping command
# Host: 192.168.142.44 - Sudoer User: aline - Permission: ALL=(ALL:ALL) ALL
# Host: 192.168.142.44 - Sudoer User: tomas - Permission: ALL = ALLNOPASSWD: ALL
# Host: 192.168.142.44 - Sudoer User: %sudoersGroup - Permission: ALL=(ALL:ALL) ALL
# Host: 192.168.142.44 - Root User: root
# Host is not accessible: 192.168.142.45
# Host is not accessible: 192.168.142.46
 
# ----------------------------------------------------------------------------------------------------
# Scan has been completed, please see the report /tmp/PrivilegedAccounts.xls                          
# Note: In case of errors, please review the log file: /tmp/report.log                                
# ----------------------------------------------------------------------------------------------------
