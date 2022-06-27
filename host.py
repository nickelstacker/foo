import subprocess
import threading
import time


def start():
	hostCmdStr = "/usr/local/bin/gst-launch-1.0 -v udpsrc port=5000" 
	hostCmdStr += " ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false"

	# redirect output to file to not spam the terminal
	outfile_w = open('/Users/trevorpennypacker/host_log.txt', "w")

	# start in new thread so rest doesn't hang  
	x = threading.Thread(target=executeHostCmd, args=(hostCmdStr, outfile_w))
	x.daemon = True
	x.start()

	# wait for the process to actually start
	outfile_r = open('/Users/trevorpennypacker/host_log.txt', "r")
	for i in range(30):
		log = outfile_r.read()
		if ('Setting pipeline to PLAYING ...' in log):
			return log
		time.sleep(0.1)



	return "Error: GStreamer could not be started on host"



def executeHostCmd(hostCmdStr, outfile):
	# subprocess.run(hostCmdStr.split(' '))
	subprocess.run(hostCmdStr.split(' '), stdout=outfile)



def free():
    ps = subprocess.run(['ps', '-ax'], stdout=subprocess.PIPE).stdout.decode("utf-8")

    numQuit = 0

    for process in ps.split('\n'):
        if ('gst' in process):
            pid = process.lstrip().split(' ')[0]
            subprocess.run(["kill", "-9", pid])
            numQuit += 1

    return numQuit
