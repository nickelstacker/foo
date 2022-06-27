import pathlib
import spurplus
import threading
import time
import network


# Re-try on connection failure
# sftp client and the underlying spur SshShell are automatically closed when the shell is closed.
def beginConnection(ip):

    err = 0

    shell = spurplus.connect_with_retries(hostname=ip, username='pi', password='meam520', connect_timeout=3, retries=1, retry_period=1)

    testResult = shell.run(["echo", "-n", "hello"])
    if (testResult.output == "hello"):
        print("SSH connection was not successful")
        err = 1
    return shell, err

def sendSourceCode(shell, host_ip):

    err = 0

    # bitratem = 1000000
    # bitrate = 5500000
    bitrate = 12000000
    # bitrate = 25000000
    width = 1920
    height = 1080
    # width = 1280
    # height = 720 
    # width = 640
    # height = 480
    port = 5000

    cmd_str = "gst-launch-1.0"
    cmd_str += " rpicamsrc"
    cmd_str += " bitrate=" + str(bitrate)
    cmd_str += " ! 'video/x-h264,width=" + str(width) + ",height=" + str(height) + "'"
    cmd_str += " ! h264parse"
    cmd_str += " ! queue"
    cmd_str += " ! rtph264pay config-interval=1 pt=96"
    cmd_str += " ! gdppay"
    cmd_str += " ! udpsink host=" + host_ip + " port=" + str(port)

    file_text = 'import os\nos.system("' + cmd_str + '")'

    p = pathlib.Path('/home/pi/source.py')
    shell.write_text(remote_path=p, text=file_text)

    if (shell.read_text(p) != file_text):
        print("Failed to install script on target")
        err = 1
    
    return err

def startSource(shell):
    executeSrcCmd(shell)
#        shell.spawn(['touch', 'proof'], allow_error=True, cwd='/home/pi')

#    y = threading.Thread(target=executeSrcCmd, args=(shell,))
#    y.daemon = True
#    y.start()

    
def executeSrcCmd(shell):
    shell.spawn(['python3', 'source.py'], allow_error=True, cwd='/home/pi')


def free(shell):
    ps = shell.run(["ps"]).output
    
    quitProcesses = []

    for process in ps.split('\n'):
        if ('python3' in process or 'gst-launch-1.0' in process):
            shell.run(["kill", "-9", process.lstrip().split(' ')[0]])
            quitProcesses.append(process)

    shell.close()

    
    return len(quitProcesses)








def freeSource(ip):
    shell = spurplus.connect_with_retries(hostname=ip, username='pi', password='meam520', connect_timeout=3, retries=1, retry_period=1)
    shell.spawn(['python3', 'freeSource.py'], allow_error=True, cwd='/home/pi')
    










        
