from collections import OrderedDict
import time
from concurrent import futures
import os
import binascii
import sqlite3

class Exploit:
	def __init__(self, uid, name, kind, code):
		self.uid = uid
		self.name = name
		self.kind = kind
		self.code = code
		self.statuses = {ip: 'error' for ip in ips}
		self.tooltips = {ip: 'No yet run' for ip in ips}

	def run(self, ip, sendone):
		self.tooltips[ip] = ''
		self.statuses[ip] = 'working'
		sendone(self.to_dict())
		local = {}
		try:
			exec(self.code + '\nresult = exploit(ip)', {'ip': ip}, local)
		except Exception as e:
			print(e)
			self.statuses[ip] = 'error'.format(e)
			self.tooltips[ip] = str(e)
		else:
			flag = local['result']
			if flag != None:
				submit(flag)
				self.statuses[ip] = 'success'
			else:
				self.statuses[ip] = 'no-flag'
		sendone(self.to_dict())

	def __repr__(self):
		return 'Exploit({}, {}, {})'.format(self.uid, self.name, self.kind)

	def to_dict(self):
		statuses = [self.statuses[ip] for ip in ips]
		tooltips = [self.tooltips[ip] for ip in ips]
		return { 'uid': self.uid,
				 'name': self.name, 
				 'type': self.kind, 
				 'statuses': statuses, 
				 'tooltips': tooltips }


def submit(flag):
	pass

def add_exploit(name, kind, code, uid = None):
	if len(name) == 0 or len(kind) == 0:
		return
	gen_uid = uid or str(binascii.b2a_hex(os.urandom(8)), encoding='utf-8')
	exploit = Exploit(gen_uid, name, kind, code)
	print('created exploit: {}'.format(exploit))
	exploits[gen_uid] = exploit
	if not uid:
		print('adding exploit to database')
		cur = db.cursor()
		cur.execute('INSERT INTO exploits VALUES (?, ?, ?, ?)',
				     (gen_uid, name, kind, code))
		db.commit()

	return exploit

def delete_exploit(uid):
	exploits.pop(uid)
	cur = db.cursor()
	cur.execute('DELETE FROM exploits WHERE uid = ?', (uid,))
	db.commit()

def get_exploit(uid):
	return exploits[uid]

def get_exploits():
	return [exploit.to_dict() for exploit in exploits.values()]

def add_ip(ip):
	if ip not in ips:
		ips.append(ip)

def delete_ip(ip):
	ips.remove(ip)

ips = ['10.0.64.27', 'localhost', '127.0.0.1', '192.168.0.1'];
exploits = OrderedDict()
interval = 5

db = sqlite3.connect('exploits.db')

def load_exploits():
	print('loading exploits from db')
	cur = db.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS exploits \
				 (uid TEXT PRIMARY KEY, name TEXT, kind TEXT, code TEXT);')
	db.commit()
	for exploit in cur.execute('SELECT * FROM exploits'):
		print('loading exploit from database: {}'.format(exploit))
		add_exploit(exploit[1], exploit[2], exploit[3], uid=exploit[0])

def launch(interval, sendall, sendone):
	load_exploits()
	while True:
		time.sleep(interval)
		with futures.ThreadPoolExecutor(4) as executor:
			running_exploits = []
			for exploit in exploits.values():
				for ip in ips:
					future = executor.submit(exploit.run, ip, sendone)
					running_exploits.append(future)
			for future in futures.as_completed(running_exploits):
				exploit = future.result()
		sendall(get_exploits())
