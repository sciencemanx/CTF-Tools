#!/usr/bin/python

import importlib, os, threading, argparse, json

import scheduler

exploitdir = 'exploits'
path = os.path.join(os.getcwd(), exploitdir)

def auto_load(interval=5):
	threading.Timer(interval, auto_load).start()
	for f in os.listdir(path):
		module = '{}.{}'.format(exploitdir, f.split('.')[0])
		importlib.import_module(module)
	with open('conf.json', 'r') as f:
		conf = json.loads(f.read())
	scheduler.ips = conf["ips"]

auto_load()
scheduler.launch()
