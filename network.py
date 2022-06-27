from subprocess import run


def getDevices():
	cmd = ['arp', '-na']
	retBytes = run(cmd, capture_output=True).stdout
	retString = retBytes.decode("utf-8")
	retLines = retString.split("\n")

	return retLines


def getSourceIP(devices):
	err = 0

	for device in devices:

		if ('at ' not in device):
			continue

		macAddress = device.split('at ')[1].split(' ')[0]

		if (isPiMacAddress(macAddress)):
			return str(device.split('(')[1].split(')')[0]), err
			
	
	# if this point is reached, MAC is not found
	# try the first (incomplete)
	for device in devices:
		if ('(incomplete)' in device):
			return str(device.split('(')[1].split(')')[0]), err

	err = 1
	return "Cannot find IP address of Pi", err


macPrefixes = ['B8:27:EB', 'B8-27-EB', 'B827.EB', 
			   'DC:A6:32', 'DC-A6-32', 'DCA6.32', 
			   'E4:5F:01', 'E4-5F-01', 'E45F.01',
			   'E4:5F:1']

def isPiMacAddress(macAddress):

	if (macAddress[0:8].upper() in macPrefixes):
		return True
	if (macAddress[0:7].upper() in macPrefixes):
		return True

	return False

def getHostIP():
	err = 0
	cmd = ['ipconfig', 'getifaddr', 'en0']
	retBytes = run(cmd, capture_output=True).stdout
	retString = retBytes.decode("utf-8").split("\n")[0]

	if ('192.168.' not in retString):
		err = 1
		return "Cannot find IP address of this Mac", err

	return str(retString), err

