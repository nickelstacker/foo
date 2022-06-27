import subprocess

def hello():
    return "Hello world from a Python script!"

def checkBrew():
	result = subprocess.run(['brew', '--version'], stdout=subprocess.PIPE)
	return(result.stdout)


def checkGstreamer():

	required_libs = ['gst-libav', 'gst-plugins-bad', 'gst-plugins-base',
				'gst-plugins-good', 'gst-plugins-ugly', 'gstreamer']

	missing_libs = []

	result = subprocess.run(['brew', 'list'], stdout=subprocess.PIPE).stdout.decode('utf-8')

	for required_lib in required_libs:
		if required_lib not in result:
			missing_libs.append(required_lib)

	return missing_libs


# res = checkGstreamer()
# print(res)