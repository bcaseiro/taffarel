###########################################################
# FAQ:
#
# 1) What it does?
# It will identify two type of Privileged Users on Linux/Unix systems. Root Users (ID 0) and Users who have some sort of sudoer's privilege. The results will be printed on the screen and also exported to a .XLS # file called PrivilegedAccounts.xls on the /tmp/ directory.
#
# 2) Why this name "taffarel"? 
# The insipiration was a goalkeeper - https://www.youtube.com/watch?v=HlCGkxgQ56c
# 
# 3) Why I wrote this tool?
# The goal is to assist sysadmins and IT auditors to identify privileged accounts in the environment so they can protect them accordingly. 
#
# 4) Can I modify this tool?
# Absolutely.
#
# 5) How do I install it?
# Just download the tool (taffarel.py) and copy it to a folder in your Linux system. 
# I developed this tool using Kali Linux version: Linux kali 4.13.0-kali1-amd64 #1 SMP Debian 4.13.10-1kali2 (2017-11-08) x86_64 GNU/Linux
#
# 6) How do I run this tool?
# Type: "python taffarel.py -h" for more information.
#
# Usage..: 
# taffarel.py <IP Address> ==> taffarel.py 192.168.142.20 
# taffarel.py <hostname> ==> taffarel.py server01
# taffarel.py <FQDN> ==> taffarel.py server01.btlab.ca
# taffarel.py <CIDR Notation> ==> taffarel.py 192.168.142.0/24
*******************************
# Author: Bruno Caseiro (bacaseiro@gmail.com)
#################################################
