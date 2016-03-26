#can't import anything sorry!, but have access to requests, itertools, socket, urllib2, re the normal way

flag_re = re.compile(r'[0-9A-Fa-F]{32}')
def exploit(ip): #takes an ip as a string
	page = requests.get('vulnerable.com/hack').text
	flag = flag_re.match(page)
	return flag #returns a flag as string or none if exploit failed -- don't worry about error handling