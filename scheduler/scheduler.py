import requests as r
import threading
from functools import wraps

_tasks = []
ips = []
omitted = [] #list of names of skipped exploits

def info(s):
	print('[*] {}'.format(s))

def warn(s):
	print('[-] {}'.format(s))

def schedule(func):
	@wraps(func)
	def task_func(ip):
		flag = func(ip)
		if flag:
			info('task {} retreived flag: {} from ip: {}'.format(func.__qualname__, flag, ip))
			success = submit(flag)
			if success:
				info('task {} successfully submitted flag'.format(func.__qualname__))
			else:
				warn('task {} failed to submit flag {}'.format(func.__qualname__, flag))
		else:
			warn('task {} failed to retreive flag from ip: {}'.format(func.__qualname__, ip))
	_tasks.append(task_func)
	return task_func

def submit(flag):
	# submit logic here (probably a post request)
	pass

def launch(interval=5.0):
	threading.Timer(interval, launch).start()
	for task in _tasks:
		if task.__qualname__ in omitted:
			continue
		for ip in ips:
			threading.Thread(target=task, args=(ip,)).run()
			
