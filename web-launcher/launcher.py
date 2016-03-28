from collections import OrderedDict
# import sqlite3
import time
from concurrent import futures

class Exploit:
	def __init__(self, name, kind, code):
		self.name = name
		self.kind = kind
		self.code = code
		self.statuses = {ip: 'error' for ip in ips}
		self.tooltips = {ip: 'No yet run' for ip in ips}

	def run(self, ip, sendone):
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

	def to_dict(self):
		statuses = [self.statuses[ip] for ip in ips]
		tooltips = [self.tooltips[ip] for ip in ips]
		return {'name': self.name, 'type': self.kind, 'statuses': statuses, 'tooltips': tooltips}

# def adapt_exploit(exploit):
# 	return '{}}{{}}{{}'.format(exploit.name, exploit.kind, exploit.code)

# def convert_exploit(s):
# 	name, kind, code = s.split(b'}{')
# 	return Exploit(name, kind, code)

def submit(flag):
	pass

def add_exploit(name, kind, code):
	exploit = Exploit(name, kind, code)
	exploits[name] = exploit

def delete_exploit(name):
	exploits.pop(name)

def get_exploit(name):
	return exploits[name]

def get_exploits():
	return [exploit.to_dict() for exploit in exploits.values()]

# db = sqlite3.connect(':memory:', check_same_thread=False)

ips = ['10.0.64.27', 'localhost', '127.0.0.1', '192.168.0.1'];
exploits = OrderedDict()
interval = 5

add_exploit('SQLi', 'VULN', 'def exploit(ip): return "flage"')

def launch(interval, sendall, sendone):
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
