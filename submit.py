import sys
import os

if len(sys.argv) != 2:
	print('Usage: {} <filename>'.format(sys.argv[0]))
	sys.exit(0)

with open(sys.argv[1], 'r') as f:
	for flag in f:
		os.system("curl -d 'apikey=8abb3ebb021c734590d41c42afd498854d848644f8cc38e11d'"\
		" -d 'flag={}' https://live.cyberstakesonline.com/api/binaries/submit".format(flag))