import requests as r
import threading
from functools import wraps
import os
import json

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
			success, message = submit(flag)
			if success:
				info('task {} successfully submitted flag'.format(func.__qualname__))
			else:
				warn('task {} failed to submit flag {} because {}'.format(func.__qualname__, flag, message))
		else:
			warn('task {} failed to retreive flag from ip: {}'.format(func.__qualname__, ip))
	_tasks.append(task_func)
	return task_func

def submit(flag):
	res = r.post('https://live.cyberstakesonline.com/liveapi/2/submit',
				  {'apikey': '8abb3ebb021c734590d41c42afd498854d848644f8cc38e11d',
				   'flag': flag})
	res = json.loads(res.text)
	return (res['status'] == '1', res['message'])
	

def launch(interval=240):
	threading.Timer(interval, launch, args=(interval,)).start()
	for task in _tasks:
		if task.__qualname__ in omitted:
			continue
		for ip in ips:
			threading.Thread(target=task, args=(ip,)).run()
			
