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
#
# Author: Bruno Caseiro
# Email: bacaseiro@gmail.com
#########################################################################################################################################################


import os, ipaddress, sys, re, logging
import paramiko, getpass
import xlwt, termcolor
import unicodedata
from netaddr import *
import pprint



# STEP 1 - Verifica se o usuario digitou o parametro (ip or network), senao, mostra o jeito certo.
def step1_USAGE():
    if len(sys.argv) == 2:

        if sys.argv[1] == '-h' or sys.argv[1] == '-H' or sys.argv[1] == '--h' or sys.argv[1] == '--H':
            USAGE()

        else:

            ipaddress = sys.argv[1]
            regexCIDR = re.compile(r'\/\d\d')                                # Prepare to Check if the user entered a CIDR notation
            CIDRvalidada = regexCIDR.findall(ipaddress)
            ipregex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")    # Check if the user entered an IP address
            hostnameregex = re.compile(r'^[a-z0-9-.]+$')                     # Check if the user entered a hostname or fqdn
           
	    ### Declaring User and Password as Global Variables to be used across all functions
	    global sshuser, sshpassword
	    sshuser = raw_input('Username: ')
	    sshpassword = getpass.getpass('Password: ')

            if regexCIDR.search(ipaddress):
		PINGAR_CIDR(ipaddress)

            # Check if the argument passed looks like an ip address (192.168.4.20)
            if ipregex.search(ipaddress):
                PINGAR_HOST_AND_IP(ipaddress)


            # Check if the argument passed looks like hostname (i.e linuxsrv, linuxsrv04, etc)
            if hostnameregex.search(ipaddress):
                print ('Hostname entered: ', ipaddress)
                PINGAR_HOST_AND_IP(ipaddress)
  
    else:
        USAGE()


############################## Funcao USAGE
def USAGE():
        print ("*******************************")
        print ("Usage..: \ntaffarel.py <IP Address> ==> taffarel.py 192.168.142.20 \ntaffarel.py <hostname> ==> taffarel.py server01\ntaffarel.py <FQDN> ==> taffarel.py server01.btlab.ca\ntaffarel.py <CIDR Notation> ==> taffarel.py 192.168.142.0/24")
        print ("*******************************")
        print (" >>> By Bruno Caseiro -- bacaseiro@gmail.com <<< ")
        print (" ")
        sys.exit()




########################### Funcao PINGAR hosts e IPs somente
# STEP 2- Verifica se Todos os hosts estao ativos na rede e loga os que estao ativos e nao ativos/disponiveis na rede.


def PINGAR_HOST_AND_IP(ipaddress):
    print (' ')
    print ('----------------------------------------------------------------------------------------------------')
    print ('Finding Privileged Users on the host: ' + str(ipaddress) + ' ---------------        Please wait     ')
    print ('----------------------------------------------------------------------------------------------------')
    print (' ')
    pingreply = os.system("ping -b -c 2 -W 2 " + ipaddress + ">/dev/null")
    logging.basicConfig(filename='/tmp/report.log',level=logging.DEBUG, format='%(asctime)s %(message)s')

    if pingreply == 0:
        print ('Host: ' + str(ipaddress) + ' responded successfully to the ping command.')
        logging.debug('PING was successful on host: ' + ipaddress)
        CONEXAO_SSH(ipaddress)
       
    else:
        print ('Host is not accessible: ' + str(ipaddress))
        logging.debug('PING failed on host: ' + ipaddress)
    sys.exit()



############################# Funcao Pingar CIDR
def PINGAR_CIDR(ipaddress):

    sudoersrow = 3
    sudoerscol = 0

    wb = xlwt.Workbook()
    sheet1 = wb.add_sheet('Taffarel - Sudoers')
    style2 = xlwt.easyxf('pattern: pattern solid, fore_colour dark_blue;' 'font: colour white, bold True;')
    # Titulo
    sheet1.write_merge(0, 0, 0, 2, 'Privileged User Discovery for Linux/Unix', style2)        

    # Cabecalho
    sheet1.write(2, 0, 'Hostname', style2)
    sheet1.write(2, 1, 'Username or Group', style2)
    sheet1.write(2, 2, 'Privilege', style2)
	
    sudoersfile = []
    rootusers = []
    segrega = []
    segregaRootUsers = []
    print (' ')
    print ('----------------------------------------------------------------------------------------------------')
    print ('Finding Privileged Users on the network: ' + str(ipaddress) + ' -------------       Please wait     ')
    print ('----------------------------------------------------------------------------------------------------')
    print (' ')

    for ip in IPNetwork(ipaddress).iter_hosts():
	
	pingreply = os.system("ping -c 1 -W 2 " + str(ip) + ">/dev/null")
    	logging.basicConfig(filename='/tmp/report.log',level=logging.DEBUG, format='%(asctime)s %(message)s')

    	if pingreply == 0:
        	print ('Host ' + str(ip) + ' responded successfully to the ping command')
        	logging.debug('PING was successful on host: ' + str(ip))
        	try:
			#Establish the SSH session
    			ssh=paramiko.SSHClient()
    			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    			#Conecta
			sshport = 22
    			ssh.connect(str(ip),port=sshport,username=sshuser,password=sshpassword)

			comando1='sudo cat /etc/sudoers | egrep -v ^#.* | egrep -v ^Defaults.* |awk NF'
			comando2='cat /etc/passwd | grep 0:0'
    			#Executa o comando1
    			stdin,stdout,stderr=ssh.exec_command(comando1)

			#Resultado comando1
    			resultadosudoers = stdout.readlines()
			if len(resultadosudoers) == 0:
				print ('User: ' + sshuser + ' cannot access the /etc/sudoers file on the host: ' + str(ip))
				logging.debug('User dos not have the necessary rights to access teh sudoers file on the host: ' + str(ip))
				continue

    			result_comando1=[]
    			result_comando1= ''.join(resultadosudoers)

			
			#Executa o comando2
    			stdin,stdout,stderr=ssh.exec_command(comando2)
    			
    			#Resultado comando2
    			resultadosID0 = stdout.readlines()
    			result_comando2=[]
    			result_comando2 = ''.join(resultadosID0)
			
			comando1_em_string = unicodedata.normalize('NFKD', result_comando1).encode('ascii','ignore') # Convertendo o comando de Unicode para String para poder usar split
			comando2_em_string = unicodedata.normalize('NFKD', result_comando2).encode('ascii','ignore') # Convertendo o comando de Unicode para String para poder usar split

			sudoersfile = comando1_em_string.split('\n')
			rootusers = comando2_em_string.split('\n')


			for linha in sudoersfile:
	    			segrega = linha.split('\t')
	    			#print (segrega[0])
	
            			for item in segrega[0]:
            			# Registros
                    			sheet1.write(sudoersrow, sudoerscol, str(ip))
                    			sheet1.write(sudoersrow, sudoerscol + 1, segrega[0])
                    			sheet1.write(sudoersrow, sudoerscol + 2, segrega[1:])
                    			sudoersrow = sudoersrow + 1
					limpa = segrega[1:]
					limpa2 = ''.join(limpa)
					print ('Host: ' + str(ip) + ' - Sudoer User: ' + str(segrega[0]) + ' - Permission: ' + limpa2)
                    			break
			
			for linhaRootUsers in rootusers:
	    			segregaRootUsers = linhaRootUsers.split(':')
	    			#print (segregaRootUsers[0])
	
            			for itemRootUsers in segregaRootUsers[0]:
            			# Registros
                    			sheet1.write(sudoersrow, sudoerscol, str(ip))
                    			sheet1.write(sudoersrow, sudoerscol + 1, segregaRootUsers[0])
                    			sheet1.write(sudoersrow, sudoerscol + 2, 'Root User - User ID is 0')
                    			sudoersrow = sudoersrow + 1
					print ('Host: ' + str(ip) + ' - Root User: ' + str(segregaRootUsers[0]))
                    			break

            			wb.save('/tmp/PrivilegedAcccounts.xls')

    			# Loga o comando no log
    			logging.debug('Conexao SSH funcionou no servidor: ' + str(ip))
    			logging.debug('<<< Running the command: >>>: ' + comando1)
			logging.debug('<<< Running the command: >>>: ' + comando2)
			

		
		except paramiko.AuthenticationException:
                  	print ("Authentication Failed - Check if the username or password is valid and if the host can be reached via SSH.")
                  	logging.debug('<<< SSH Authentication Failed >>>: ' + sshuser + ' on host' + str(ip))


    		except paramiko.ssh_exception.NoValidConnectionsError:
                  	print ("Unable to connect to the SSH port on the target system: " + str(ip))
                  	logging.debug("<<< Unable to connect to the SSH port on the target system >>> : " + str(ip))
    		

       	else:
        	print ('Host is not accessible: ' + str(ip))
        	logging.debug('PING failed on host: ' + str(ip))

    print (' ')
    print ('----------------------------------------------------------------------------------------------------')
    print ('Scan has been completed, please see the report /tmp/PrivilegedAccounts.xls                          ')
    print ('Note: In case of errors, please review the log file: /tmp/report.log                                ')
    print ('----------------------------------------------------------------------------------------------------')
    print ('                 by Bruno Caseiro - bacaseiro@gmail.com                                  ')
    print ('----------------------------------------------------------------------------------------------------')
    print (' ')

#----------------- FIM Do block CIDR check -----------------------------------------_#
	


############################## Funcao Conexao SSH
def CONEXAO_SSH(ipaddress):
      
    try:

	comando1='sudo cat /etc/sudoers | egrep -v ^#.* | egrep -v ^Defaults.* |awk NF'
    	comando2='cat /etc/passwd | grep 0:0'
    	sshport = 22

    	#Establish the SSH session
    	ssh=paramiko.SSHClient()
    	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    	#Conecta
    	ssh.connect(ipaddress,port=sshport,username=sshuser,password=sshpassword)

    	#Executa o comando1
    	stdin,stdout,stderr=ssh.exec_command(comando1)

    	# Loga o comando no log
    	logging.debug('Conexao SSH funcionou no servidor: ' + ipaddress)
    	logging.debug('<<< Running the command: >>>: ' + comando1)
    
    	#Resultado comando1
    	resultadosudoers = stdout.readlines()

	if len(resultadosudoers) == 0:
			print ('User: ' + sshuser + ' cannot access the /etc/sudoers file on the host: ' + str(ipaddress))
			logging.debug('User dos not have the necessary rights to access teh sudoers file on the host: ' + str(ipaddress))
			print (' ')
			sys.exit()
    	result_comando1=[]
    	result_comando1= ''.join(resultadosudoers)
	
    	#Executa o comando2
    	stdin,stdout,stderr=ssh.exec_command(comando2)
    	logging.debug('<<< Running the command: >>>: ' + comando2)
    	#Resultado comando2
    	resultadosID0 = stdout.readlines()
    	result_comando2=[]
    	result_comando2 = ''.join(resultadosID0)
    	
    	# Fecha a Sessao SSH
    	ssh.close()

	
########################## Excel Report (Single IP or hostname)
	comando1_em_string = unicodedata.normalize('NFKD', result_comando1).encode('ascii','ignore') # Convertendo o comando de Unicode para String para poder usar split
	comando2_em_string = unicodedata.normalize('NFKD', result_comando2).encode('ascii','ignore') # Convertendo o comando de Unicode para String para poder usar split

        sudoersfile = []
        sudoersfile = comando1_em_string.split('\n')

	rootusers = []
	rootusers = comando2_em_string.split('\n')

        sudoersrow = 3
        sudoerscol = 0

        wb = xlwt.Workbook()
        sheet1 = wb.add_sheet('Taffarel - Sudoers')

	style2 = xlwt.easyxf('pattern: pattern solid, fore_colour dark_blue;' 'font: colour white, bold True;')


        # Titulo
	sheet1.write_merge(0, 0, 0, 2, 'Privileged User Discovery for Linux/Unix', style2)        

        # Cabecalho
	sheet1.write(2, 0, 'Hostname', style2)
        sheet1.write(2, 1, 'Username or Group', style2)
        sheet1.write(2, 2, 'Privilege', style2)

  
########## Excel Sudoers File
	segrega = []
	segregaRootUsers = []

	for linha in sudoersfile:
	    segrega = linha.split('\t')
	    	
            for item in segrega[0]:
            # Registros
                    sheet1.write(sudoersrow, sudoerscol, ipaddress)
                    sheet1.write(sudoersrow, sudoerscol + 1, segrega[0])
                    sheet1.write(sudoersrow, sudoerscol + 2, segrega[1:])
                    sudoersrow = sudoersrow + 1
		    limpa = segrega[1:]
		    limpa2 = ''.join(limpa)
		    print ('Host: ' + str(ipaddress) + ' - Sudoer User: ' + str(segrega[0]) + ' - Permission: ' + limpa2)
                    break


########## Users with ID 0 - Root Users
	for linhaRootUsers in rootusers:
	    segregaRootUsers = linhaRootUsers.split(':')
	    	
            for itemRootUsers in segregaRootUsers[0]:
            # Registros
                    sheet1.write(sudoersrow, sudoerscol, ipaddress)
                    sheet1.write(sudoersrow, sudoerscol + 1, segregaRootUsers[0])
                    sheet1.write(sudoersrow, sudoerscol + 2, 'Root User - User ID is 0')
                    sudoersrow = sudoersrow + 1
		    print ('Host: ' + str(ipaddress) + ' - Root User: ' + str(segregaRootUsers[0]))
                    break

            wb.save('/tmp/PrivilegedAcccounts.xls')
	print (' ')
    	print ('----------------------------------------------------------------------------------------------------')
    	print ('Scan has been completed, please see the report /tmp/PrivilegedAccounts.xls                          ')
    	print ('Note: In case of errors, please review the log file: /tmp/report.log                                ')
	print ('----------------------------------------------------------------------------------------------------')
    	print ('                 by Bruno Caseiro - bacaseiro@gmail.com                                  ')
    	print ('----------------------------------------------------------------------------------------------------')
	print (' ')

########################## End of the Excel Report

    except paramiko.AuthenticationException:
                  print ("<<< Authentication Failed >>>: Check if the username or password is valid and if the host can be reached via SSH.")
                  logging.debug('<<< SSH Authentication Failed >>>: ' + sshuser + ' on host' + ipaddress)


    except paramiko.ssh_exception.NoValidConnectionsError:
                  print ("<<< Unable to connect to the SSH port on the target system >>> : " + ipaddress)
                  logging.debug("<<< Unable to connect to the SSH port on the target system >>> : " + ipaddress)



step1_USAGE()
