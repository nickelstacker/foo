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
#       ######### BEGIN SSH CONNECTION #########
#       ########################################
shell, err = ssh.beginConnection(source_ip)
if (err):
    print("Terminating process (3)")
    exit()


#       ########################################
#       ######## START SOURCE PROCESS ##########
#       ########################################
num_quit = ssh.free(shell)
print("Terminated " + str(num_quit) + " processes on source")