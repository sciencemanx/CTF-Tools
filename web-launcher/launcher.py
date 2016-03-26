ips = ['10.0.64.27', 'localhost', '127.0.0.1', '192.168.0.1'];
exploits = []
interval = 10

class Exploit:
	def __init__(self, name, kind, code):
		self.name = name
		self.kind = kind
		self.code = code
		self.statuses = {ip: 'no-flag' for ip in ips}

	def run(self, ip):
		local = {}
		try:
			exec(self.code + '\nresult = exploit(ip)', {'__builtins__': {}, 'ip': ip}, local)
		except Exception as e:
			print(e)
		flag = local['result']
		if flag != None:
			submit(flag)
			self.statuses[ip] = 'success'
		else:
			self.statuses[ip] = 'no-flag'

	def to_dict(self):
		statuses = [self.statuses[ip] for ip in ips]
		return {'name': self.name, 'type': self.kind, 'statuses': statuses}



def submit(flag):
	pass

def add_exploit(name, kind, code):
	exploit = Exploit(name, kind, code)
	exploits.append(exploit)

def get_exploits():
	return [exploit.to_dict() for exploit in exploits]

add_exploit('SQLi', 'VULN', 'def exploit(ip): return "flage"')
for exploit in exploits:
	for ip in ips:
		exploit.run(ip)