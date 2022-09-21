# importing Flask and other modules
from os import name
from re import T
import re
from flask import Flask, request, render_template, redirect,url_for, flash, session, abort, jsonify
import requests, json
from werkzeug import datastructures
import auxMethods
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
		data= auxMethods.setObject4Server(request.form,"nif" ,"pin")
		headers = {'Content-Type': 'application/json'}
		req = requests.post('http://'+host+':5000/login', json=data, verify=False, headers=headers)
		
		token = req.json()
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
		data = auxMethods.setObject4Server(request.form, "nif","nombre","apellido1","apellido2","instrumento","tlf","pin")
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
			data = auxMethods.setObject4Server(request.form, "nif","nombre","apellido1","apellido2","instrumento","tlf","pin")
			headers = {'Content-Type': 'application/json'}
			req = requests.post('http://'+host+':5000/addUser', json=data, verify=False, headers=headers )
			array=req.json()
			error=array.get('error')
			data=array.get('data')

			return render_template('addUser.html', json=data, error=error ,succes=True)  # Added param error message to retrieve the error message from the server in the html
		return render_template('addUser.html', json=data, error=error,succes=False)
		
#/////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/addBanda', methods =["GET", "POST"])
def registerBanda():
	global token
	if(token == None):
			return redirect('/')
	else:
		error=""
		data=""

		if(request.method == 'POST'):
			data= auxMethods.setObject4Server(request.form, "nombre", "poblacion")
			headers = {'Content-Type': 'application/json'}
			req = requests.post('http://'+host+':5000/addBanda', json=data, verify=False, headers=headers )
			array=req.json()
			error=array.get('error')
			data=array.get('data')

			return render_template('addBanda.html', json=data, error=error ,succes=True)  # Added param error message to retrieve the error message from the server in the html
		return render_template('addBanda.html', json=data, error=error,succes=False)
#/////////////////////////////////////////////////////////////////////////////////////////////////		 
@app.route('/listMembers', methods = ['GET' , 'HEAD'])
def getMembers():
	global token
	if(token != None):
		if request.method == "GET":
			req = requests.get('http://'+host+':5000/listMembers')
			llista = req.json()
			return render_template('listMembers.html', users=llista, len=len(llista))
		else:
			return redirect('/')
#/////////////////////////////////////////////////////////////////////////////////////////////////		 
@app.route('/listBandas', methods = ['GET' , 'HEAD'])
def getBandas():
	global token
	if(token != None):
		if request.method == "GET":
			req = requests.get('http://'+host+':5000/listBandas')
			lista = req.json()
			return render_template('listBandas.html', bandas=lista, len=len(lista))
		else:
			return redirect('/')
#/////////////////////////////////////////////////////////////////////////////////////////////////		 TODO
@app.route('/joinBanda', methods =["POST" , "GET"])
def joinner():
	global token
	if(token != None):
		if request.method == "GET":
			data= {"token":token}
			headers = {'Content-Type': 'application/json'}
			req = requests.get('http://'+host+':5000/listJoin', json=data, verify=False, headers=headers )
			llista = req.json()
			return render_template('join.html', banda=llista, len=len(llista)) 
			
		if request.method == "POST":
			id = request.form.get("id")
			data= {
				"token":token,
				"id":id
				}
			headers = {'Content-Type': 'application/json'}
			req = requests.post('http://'+host+':5000/join', json=data , verify=False, headers=headers)
			return redirect("/joinBanda")
		return render_template('join.html')
	else:
		return redirect('/')
#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
@app.route('/leaveBanda', methods =["GET", "POST"])
def leaver():
	global token
	if(token != None):
		if request.method == "GET":

			data={"token":token}
			headers = {'Content-Type': 'application/json'}
			req = requests.get('http://'+host+':5000/listLeave', json=data, verify=False, headers=headers )
			llista = req.json()
			return render_template('leave.html', banda=llista, len=len(llista))
			
		if request.method == "POST":
			data={
				"token":token,
				"id" : request.form.get('id')
			}
			headers = {'Content-Type': 'application/json'}
			req = requests.post('http://'+host+':5000/leave', json=data , verify=False, headers=headers)
			return redirect("/leaveBanda")
		return render_template('leave.html')
	else:
		return redirect('/')
#/////////////////////////////////////////////////////////////////////////////////////////////////		
@app.route('/addEvent', methods =["GET", "POST"])
def addEvent():
	global token
	if(token == None):
			return redirect('/')
	else:
		error=""
		data=""

		if(request.method == 'POST'):
			data= auxMethods.setObject4Server(request.form, "nombre", "ubicacion","fecha_evento")
			headers = {'Content-Type': 'application/json'}
			req = requests.post('http://'+host+':5000/addEvent', json=data, verify=False, headers=headers )
			array=req.json()
			error=array.get('error')
			data=array.get('data')

			return render_template('addEvent.html', json=data, error=error ,succes=True)  # Added param error message to retrieve the error message from the server in the html
		return render_template('addEvent.html', json=data, error=error,succes=False)
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listEvents', methods = ['GET' , 'HEAD'])
def getEvents():
	global token
	if(token != None):
		if request.method == "GET":
			req = requests.get('http://'+host+':5000/listEvents')
			lista = req.json()
			return render_template('listEvents.html', eventos=lista, len=len(lista))
		else:
			return redirect('/')
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__=='__main__':
	app.run(debug=True, port=3000)
