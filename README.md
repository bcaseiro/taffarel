########################################################################################################################################################
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
#*******************************
#Usage..: 
#python taffarel.py 192.168.142.20 
#python taffarel.py server01
#python taffarel.py server01.btlab.ca
#python taffarel.py 192.168.142.0/24
#Author: Bruno Caseiro (bacaseiro@gmail.com) 
#########################################################################################################################################################
