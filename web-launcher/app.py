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
		launcher.add_exploit(name, 'HTTP', code)
		return redirect(url_for('launcher_status'))

@app.route('/editexploit/<name>')
def edit_exploit(name):
	exploit = launcher.get_exploit(name)
	return render_template('addexploit.html', addedit='Edit', exploit=exploit)

@socketio.on('connect', namespace='/ws')
def connected():
	update_exploits(launcher.get_exploits())
	update_ips()

def update_exploit(exploit):
	socketio.emit('exploit', exploit, namespace='/ws')

def update_exploits(exploits):
	socketio.emit('exploits', exploits, namespace='/ws')

def update_ips():
	socketio.emit('ips', launcher.ips, namespace='/ws')

if __name__ == '__main__':
	thread = Thread(target=launcher.launch, args=(5, update_exploits, update_exploit))
	thread.daemon = True
	thread.start()
	socketio.run(app, debug=True)
	