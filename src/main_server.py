from ctypes.wintypes import PINT
from re import T, X
from readline import append_history_file
from psutil import net_if_addrs
from psycopg2 import apilevel
import requests
from datetime import date
from os import strerror
import socket,sqlite3,time,json,sys,threading, os, signal
from _thread import *
from sqlite3.dbapi2 import Date, Row
from sqlite3 import Error
from datetime import datetime
from requests.sessions import RequestsCookieJar
import auxMethods
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def connection():
    try:
        con = sqlite3.connect('database.db')
        return con
    except Error:
        print(Error)
        
#/////////////////////////////////////////////////////////////////////////////////////////////////		 
@app.route('/greetings', methods=["GET"])
def greetings():
    if request.method == "GET":
        response = request.data
        array=json.loads(response.decode('utf-8'))
        token = array.get('token')
        nombre = auxMethods.getUserNameFromid(token)
        apellido1 = auxMethods.getUserSurname1Fromid(token)
        apellido2 = auxMethods.getUserSurname2Fromid(token)
        ret = json.dumps({'nombre':nombre,'apellido1':apellido1 ,'apellido2':apellido2 })
        return ret

#/////////////////////////////////////////////////////////////////////////////////////////////////		 DONE
@app.route('/login', methods =["GET", "POST"])
def login():
    
    if request.method == "POST":
        response = request.data
        array=json.loads(response.decode('utf-8'))
        nif= array.get('nif')
        pin= array.get('pin') 

        ret = login(nif,pin )
        print ("ret \n")
        print (ret)

        return ret
		
def login(nif, pin):                                                           #Method to log in on de website
    token = None
    con= connection()
    print(con)
    query = 'SELECT id, nif, pin, nombre FROM Miembro'
    for row in auxMethods.getCursor(con).execute(query):
            if(row[1] == int(nif) and str(row[2]) == str(pin) ):
                    token= row[0]
                    ret = json.dumps(token)
                    return ret  # with the return here, the loop stops when it smash the match (no innecesary iterations) 
    con.close()
    ret = json.dumps(token)
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////		 
@app.route('/addUser', methods =["POST"])
def registerUser():
    if(request.method=="POST"):
        response = request.data
        array=json.loads(response.decode('utf-8'))
        nif= array.get('nif')
        nombre=array.get('nombre') 
        apellido1=array.get('apellido1')
        apellido2=array.get('apellido2')
        instrumento=array.get('instrumento')    
        tlf=  array.get('tlf')
        pin=array.get('pin')
        return addUser(nif,nombre,apellido1,apellido2,instrumento,tlf,pin)


def addUser(nif,nombre,apellido1,apellido2,instrumento,tlf,pin):                                     # Method for add a User to the database 
    con = connection()
    for row in auxMethods.getCursor(con).execute('SELECT nif FROM Miembro'):
        if(row[0] ==nif):
            print("HELLOO")
            data =  "El usuario ya existe"
            ret = json.dumps({'data':data, 'error':True})                                              # Check if the user already exists by using the email
            return ret
    id = lambda : str(round(time.time()*1000))  # Get a rabndom number for the id of the user if does not exist already use ord() to convert from ASCII  char to number added to id unique
    print("lamda ok")
    query = 'INSERT INTO Miembro (id,nif,nombre,apellido1,apellido2,instrumento,tlf,pin) VALUES (%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s")'%(id,nif,nombre,apellido1,apellido2,instrumento,tlf,pin)
   # test for the query to pass params {nif} {nombre}...
    auxMethods.getCursor(con).execute(query)
    con.commit()
    con.close()
    data = "Miembro añadido correctamente"
    ret = json.dumps({'data':data, 'error':False})                                              # Check if the user already exists by using the email
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////       

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__=='__main__':
	app.run(debug=True, host="127.0.0.1")
