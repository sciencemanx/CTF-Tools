from flask import Flask, url_for, render_template, request, redirect
from flask_socketio import SocketIO, emit
from threading import Thread

#needed due to background thread
import eventlet
eventlet.monkey_patch()

import launcher

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shh! its a secret'
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def launcher_status():	
	return render_template('index.html', id='exp')

@app.route('/addexploit', methods=['GET', 'POST'])
def add_exploit():
	if request.method == 'GET':
		return render_template('addexploit.html', id='addexp', addedit='Add')
	else:
		name = request.form['name']
		code = request.form['code']
		kind = request.form['kind']
		launcher.add_exploit(name, kind, code)
		return redirect(url_for('launcher_status'))

@app.route('/editexploit/<name>')
def edit_exploit(name):
	exploit = launcher.get_exploit(name)
	return render_template('addexploit.html', addedit='Edit', exploit=exploit)

@app.route('/ips')
def ips():
	return render_template('ips.html', id='ips')

@socketio.on('connect', namespace='/ws')
def connected():
	update_exploits(launcher.get_exploits())
	update_ips()

@socketio.on('delete-exploit', namespace='/ws')
def delete_exploit(json):
	print('deleting exploit')
	name = json['name']
	launcher.delete_exploit(name)
	update_exploits(launcher.get_exploits())

@socketio.on('add-ip', namespace='/ws')
def add_ip(json):
	ip = json['ip']
	launcher.add_ip(ip)
	update_ips()

@socketio.on('delete-ip', namespace='/ws')
def delete_ip(json):
	ip = json['ip']
	launcher.delete_ip(ip)
	update_ips()

def update_exploit(exploit):
	socketio.emit('exploit', exploit, namespace='/ws')

def update_exploits(exploits):
	socketio.emit('exploits', exploits, namespace='/ws')

def update_ips():
	socketio.emit('ips', launcher.ips, namespace='/ws')

def main():
	thread = Thread(target=launcher.launch, args=(5, update_exploits, update_exploit))
	thread.daemon = True
	thread.start()
	socketio.run(app, debug=True)

if __name__ == '__main__':
	main()
	