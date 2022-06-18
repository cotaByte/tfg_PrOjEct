# importing Flask and other modules
from os import name
from re import T
import re
from flask import Flask, request, render_template, redirect
import requests, json
from werkzeug import datastructures
# Flask constructor

token = None
app = Flask(__name__)


#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
@app.route('/', methods =["GET"])
def index():
	return render_template('index.html')

host = 'localhost'

@app.route('/login', methods =["GET", "POST"])
def login():
	global token
	if request.method == "POST":
		nif = request.form.get("nif")
		pin = request.form.get("pin")

		data = {
			"nif": nif, 
			"pin": pin,
    	}

		headers = {'Content-Type': 'application/json'}
		req = requests.post('http://'+host+':5000/login', json=data, verify=False, headers=headers)
		
		token = req.json()
		if(token != None):
			return redirect('/greetings')

	return render_template('login.html')
#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
@app.route('/logout', methods =["POST"])
def logout():
	global token
	token = None
	return redirect('/')

#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
@app.route('/greetings', methods =["GET", "HEAD"])
def menu():
	global token
	if request.method == "GET":
		if(token != None):
			data = {
				'token':token
			}
			headers = {'Content-Type': 'application/json'}
			req = requests.get('http://'+host+':5000/greetings', json=data,verify=False, headers=headers)
			array=req.json()
			name=array['name']
			surname=array['surname']
			email=array['email']
			return render_template('greetings.html', name=name, surname=surname, email=email)
		else:
			return redirect('/')
#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE

#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
if __name__=='__main__':
	app.run(debug=True, port=3000)