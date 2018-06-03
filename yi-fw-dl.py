import json
import urllib.request
import urllib.parse
import argparse
import textwrap
import requests
import sys
ap = argparse.ArgumentParser()
ap.add_argument("camera",help="Camera Serial Number", action="store",type=str)
ap.add_argument("-a", help="List previous firmwares", action="store_true", default=False)
ap.add_argument("-n", help="Custom filename", action="store")
ap.add_argument("-c", help="Removes download confirmation", action="store_true", default=False)
args = vars(ap.parse_args())

def print_data(choice):
	print("SN:",j[choice]["snPrefix"],"- HW Code:",j[choice]["hardwareCode"])
	print("")
	print("Version",j[choice]["firmwareCode"],"- MD5",j[choice]["md5Code"])
	print("")
	print("Release notes:")
	print(textwrap.dedent(j[choice]["firmwareMemo"]).strip())
	print("")
	if args["c"] == False:
		print("Press enter to download", end="")
		input()
	fw_filename="firmware-"+j[choice]["firmwareCode"].replace(".","_")+".bin"
	if args["n"] != None:
		fw_filename = args["n"]
	download(j[choice]["firmwareUrl"], fw_filename)	

def download(url, fw_filename):
	with open(fw_filename, "wb") as f:
		print("Downloading %s" % fw_filename)
		response = requests.get(url, stream=True)
		total_length = response.headers.get('content-length')

		if total_length is None: # no content length header
			f.write(response.content)
		else:
			dl = 0
			total_length = int(total_length)
			for data in response.iter_content(chunk_size=4096):
				dl += len(data)
				f.write(data)
				done = int(50 * dl / total_length)
				sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
				sys.stdout.flush()
camera_url=""
if args["camera"].startswith("J"):
	camera_url="https://www.yitechnology.com/support/actionlite_input"

elif args["camera"].startswith("Z"):
	camera_url="https://www.yitechnology.com/support/action4k_input"
data = urllib.parse.urlencode({'id' : '3','sn'  : args["camera"]})
data = data.encode('utf-8')
raw = urllib.request.urlopen(camera_url, data=data).read()
if args["a"] == False:
	j=json.loads(raw)
	print_data(0)
else:
	j=json.loads(raw)
	for index, i in enumerate(j):
		print(index,"-",i["firmwareCode"])
	try:
		choice=int(input("Firmware download: [0 - " + str(len(j)-1) + "]: "))
	except ValueError:
		choice=0
	print_data(choice)
