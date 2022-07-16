# importing Flask and other modules
from os import name
from re import T
import re
from flask import Flask, request, render_template, redirect,url_for, flash, session, abort, jsonify
import requests, json
from werkzeug import datastructures
# Flask constructor

token = None
app = Flask(__name__)


#/////////////////////////////////////////////////////////////////////////////////////////////////		 DONE
@app.route('/', methods =["GET"])
def index():
	return render_template('index.html')

host = 'localhost'
#/////////////////////////////////////////////////////////////////////////////////////////////////		 DONE
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
		print(token)
		if(token != None): return redirect('/greetings')

	return render_template('login.html')
#/////////////////////////////////////////////////////////////////////////////////////////////////		 DONE
@app.route('/logout', methods =["POST"])
def logout():
	global token
	token = None
	return redirect('/')

#/////////////////////////////////////////////////////////////////////////////////////////////////		 
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
			nombre =array['nombre']
			apellido1=array['apellido1']
			apellido2=array['apellido2']
			
			return render_template('greetings.html', nombre=nombre, apellido1=apellido1, apellido2=apellido2)
		else:
			return redirect('/')
#/////////////////////////////////////////////////////////////////////////////////////////////////		 
@app.route('/register', methods =["GET", "POST"])
def register():

	if request.method == "POST":
		nif = request.form.get("nif")
		nombre = request.form.get("nombre")
		apellido1 = request.form.get("apellido1")
		apellido2 = request.form.get("apellido2")
		instrumento = request.form.get("instrumento")
		tlf = request.form.get("tlf")
		pin = request.form.get("pin")
	
		
		data = {
			"nif": nif, 
			"nombre":	 nombre,
			"apellido1": apellido1,
			"apellido2": apellido2,
			"instrumento": instrumento,
			"tlf": tlf,
			"pin": pin,
		}


		headers = {'Content-Type': 'application/json'}

		req = requests.post('http://'+host+':5000/addUser', json=data, verify=False, headers=headers)
		return redirect('/register')
	return render_template('register.html')


#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
@app.route('/addUser', methods =["GET", "POST"])
def registerUser():
	global token
	if(token == None):
		return redirect('/')
	else:
		error=""
		data=""
		if request.method == "POST":
			nif = request.form.get("nif")
			nombre = request.form.get("nombre")
			apellido1 = request.form.get("apellido1")
			apellido2 = request.form.get("apellido2")
			instrumento = request.form.get("instrumento")
			tlf = request.form.get("tlf")
			pin = request.form.get("pin")
		
			
			data = {
				"nif": nif, 
				"nombre":	 nombre,
				"apellido1": apellido1,
				"apellido2": apellido2,
				"instrumento": instrumento,
				"tlf": tlf,
				"pin": pin,
		}

			headers = {'Content-Type': 'application/json'}
			req = requests.post('http://'+host+':5000/addUser', json=data, verify=False, headers=headers )
			array=req.json()
			error=array.get('error')
			data=array.get('data')

			return render_template('addUser.html', json=data, error=error ,succes=True)  # Added param error message to retrieve the error message from the server in the html
		return render_template('addUser.html', json=data, error=error,succes=False)
		
#/////////////////////////////////////////////////////////////////////////////////////////////////		 
if __name__=='__main__':
	app.run(debug=True, port=3000)