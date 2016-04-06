#!/usr/bin/python

import importlib, os, threading, argparse, json

import scheduler

exploitdir = 'exploits'
path = os.path.join(os.getcwd(), exploitdir)

def auto_load(interval=240):
	threading.Timer(interval, auto_load, args=(interval,)).start()
	for f in os.listdir(path):
		if f == ".DS_Store": 
			continue
		module = '{}.{}'.format(exploitdir, f.split('.')[0])
		importlib.import_module(module)

	with open('conf.json', 'r') as f:
		conf = json.loads(f.read())
	print('ips: {}'.format(conf["ips"]))
	scheduler.ips = conf["ips"]
	scheduler.omitted = conf["omitted"]

auto_load(240)
scheduler.launch()
