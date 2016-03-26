from flask import Flask, url_for, render_template, request, redirect
from flask_restful import Resource, Api

import launcher

app = Flask(__name__)
api = Api(app)

@app.route('/')
def launcher_status():
	return render_template('index.html', name='exp')

@app.route('/addexploit', methods=['GET', 'POST'])
def add_exploit():
	if request.method == 'GET':
		return render_template('addexploit.html', name='addexp')
	else:
		name = request.form['name']
		code = request.form['code']
		launcher.add_exploit(name, 'HTML', code)
		return redirect(url_for('launcher_status'))

@app.route('/editexploit/<name>')
def edit_exploit(name):
	pass

class Exploits(Resource):
	def get(self):
		return launcher.get_exploits()

class IPs(Resource):
	def get(self):
		return launcher.ips

if __name__ == '__main__':
	api.add_resource(Exploits , '/exploits')
	api.add_resource(IPs, '/ips')
	app.run(debug=True)