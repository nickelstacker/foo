import ssh
import host
import network
import os

os.system('clear')

#       ########################################
#       ###### FIND ALL DEVICES ON NETWORK #####
#       ########################################
devices = network.getDevices()


#       ########################################
#       ############# FIND THE PI ##############
#       ########################################
source_ip, err = network.getSourceIP(devices)
print(source_ip)
if (err):
    print("Terminating process (1)")
    exit()


#       ########################################
#       ########## FIND THIS MACHINE ###########
#       ########################################
host_ip, err = network.getHostIP()
print(host_ip)
if (err):
    print("Terminating process (2)")
    exit()


#       ########################################
#       ######### BEGIN SSH CONNECTION #########
#       ########################################
shell, err = ssh.beginConnection(source_ip)
if (err):
    print("Terminating process (3)")
    exit()


#       ########################################
#       ###### SEND PYTHON SCRIPT TO PI ########
#       ########################################
err = ssh.sendSourceCode(shell, host_ip)
if (err):
    print("Terminating process (4)")
    exit()



#       ########################################
#       ######### START HOST PROCESS ###########
#       ########################################
err = host.start()
if (err):
    print("Terminating process (5)")
    exit()


#       ########################################
#       ######## START SOURCE PROCESS ##########
#       ########################################
ssh.startSource(shell)