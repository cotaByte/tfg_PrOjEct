from crypt import methods
from ctypes.wintypes import PINT
from curses import resetty
from mailbox import NoSuchMailboxError
from re import T, X
import re
from readline import append_history_file
from urllib import response
from psutil import net_if_addrs
import psycopg2
import requests
from datetime import date
from os import strerror
import socket,sqlite3,time,json,sys,threading, os, signal
from _thread import *
from requests.sessions import RequestsCookieJar
import auxMethods
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def connection(): # method for connecting to the database
    try :
        con = psycopg2.connect(

            host= 'localhost',
            user='postgres',
            password='password',
            database='xarangapp'
        )
        return con
    except Exception as ex:
        print(ex)


        
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
    c= auxMethods.getCursor(con)
    c.execute(query)
    for record in c:
            if(record[1] == int(nif) and str(record[2]) == str(pin) ):
                    token= record[0]
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
        director = array.get('director')
        banda = array.get('banda')
        tlf=  array.get('tlf')
        pin=array.get('pin')
        return addUser(nif,nombre,apellido1,apellido2,instrumento,director, banda,tlf,pin)


def addUser(nif,nombre,apellido1,apellido2,instrumento,director, banda,tlf,pin):                                     # Method for add a User to the database 
    con = connection()
    c= auxMethods.getCursor(con)
    query = 'SELECT nif FROM Miembro'
    c.execute(query)
    for record in c:
        if(record[0] ==nif):
            data =  "El usuario ya existe"
            con.close()
            ret = json.dumps({'data':data, 'error':True})                                              # Check if the user already exists by using the email
            return ret
    
    id = lambda a : str(round(time.time()*1000)) if director== 0 else str(round(time.time()*1000))+"D"
     # Get timestamp for the id of the user

    c.execute('INSERT INTO miembro (id, nif, nombre, apellido1, apellido2, id_instrumento, telefono, id_banda, director, pin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)'
    ,(id(director),int(nif),nombre,apellido1,apellido2,int(instrumento),int(tlf),banda,director,int(pin)))
    con.commit()
    con.close()
    data = "Miembro añadido correctamente"
    ret = json.dumps({'data':data, 'error':False})                                              # Check if the user already exists by using the email
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////       
@app.route('/addBanda', methods =[ "POST"])
def registerBanda():
    if (request.method== "POST"):
        response= request.data
        array=json.loads(response.decode('utf-8'))
        nombre= array.get('nombre')
        poblacion = array.get('poblacion')
        return addBanda(nombre,poblacion)


def addBanda(nombre,poblacion):
    con = connection()
    c= auxMethods.getCursor(con)
    query = 'SELECT nombre FROM Banda'
    c.execute(query)
    for record in c:
        if (record[0] == nombre):
            data =  "Esta banda ya se encuentra registrada"
            con.close()
            ret = json.dumps({'data':data, 'error':True})                                              # Check if the user already exists by using the email
            return ret

    id = str(round(time.time()*1000))
    c.execute('INSERT INTO banda (id_banda, nombre, poblacion) VALUES (%s, %s, %s) ', (id, nombre, poblacion ))
    con.commit()
    con.close()
    data = "Banda añadida correctamente"
    ret = json.dumps({'data':data, 'error':False})                                              # Check if the user already exists by using the email
    return ret

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listMembers', methods=['GET','HEAD'])
def getUsers():
    if (request.method== 'GET'):
        return listMembers()

def listMembers():
    con = connection()
    c = auxMethods.getCursor(con)
    c.execute("SELECT id, nombre, apellido1, apellido2,id_instrumento, telefono FROM Miembro")
    data = c.fetchall()
    print (data)
    c.close()
    ret = json.dumps(data)
    return ret
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listBandas', methods=['GET','HEAD'])
def getBandas():
    if (request.method== 'GET'):
        return listBandas()

def listBandas():
    con = connection()
    c = auxMethods.getCursor(con)
    c.execute("SELECT * FROM Banda")
    data = c.fetchall()
    print (data)
    c.close()
    ret = json.dumps(data)
    return ret
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/join', methods = [ "POST"])
def joinBanda():
    if (request.method == "POST"):
        response = request.data
        array=json.loads(response.decode('utf-8'))
        idBanda = array.get('id')
        token = array.get('token')
        ret = join (token, idBanda)
        return ret

def join (token,  idBanda):
    con = connection()
    c = auxMethods.getCursor(con)
    sql  = "SELECT nombre FROM Banda WHERE id_banda = '%s' "%idBanda
    c.execute(sql)
    for record in c:
        name = record[0]
        c.execute( "SELECT id_miembro, id_banda FROM miembrobanda WHERE id_miembro =%s AND id_banda = %s  ",(token,idBanda))
        res= None
        res= c.fetchall()
        if(res):
            con.close()
            data= "El miembro ya se encuentra en esta banda"
            ret = json.dumps(data)
            return ret
        try:
            sqlInsert = "INSERT INTO miembrobanda (id_miembro,id_banda) VALUES (%s,%s )"
            c.execute(sqlInsert,(token,idBanda))
            con.commit()
            data = "Te has añadido a la banda  "+name+" correctamente"
            con.close()
            ret = json.dumps(data)
            return ret
        except:
             con.close()
             data = "No se ha podido abandonar la banda"
             ret = json.dumps(data)
             return ret

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listJoin' , methods =[ "GET"])
def  joinLister():
    if (request.method == "GET"):
        response= request.data
        array = json.loads(response.decode('utf-8'))
        print (array)
        token = array.get("token")
        return listJoin(token)

def  listJoin(token):
    con = connection()
    c = auxMethods.getCursor(con)
    sql = " select * from banda where id_banda not in (select id_banda from miembrobanda where id_miembro= %s );"
    c.execute( sql,(token,))
    data= c.fetchall()
    print (data)
    c.close()
    ret= json.dumps(data)
    return ret
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listLeave' , methods =[ "GET"])
def leaveLister():
    if (request.method == "GET"):
        response= request.data
        array = json.loads(response.decode('utf-8'))
        token = array.get("token")
        return listLeave(token)

def  listLeave(token):
    con = connection()
    c = auxMethods.getCursor(con)
    sql = " select * from banda where id_banda in (select id_banda from miembrobanda where id_miembro= %s );"
    c.execute( sql,(token,))
    data= c.fetchall()
    print (data)
    c.close()
    ret= json.dumps(data)
    return ret
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/leave', methods = [ "POST"])
def leaveBanda():
    if (request.method  == "POST"):
        response= request.data
        array = json.loads(response.decode('utf-8'))
        idBanda = array.get ("id")
        token = array.get ("token")
        ret = leave(token,idBanda)
        return ret

def leave(token, idBanda):
    con = connection()
    query = "SELECT id_banda FROM Banda WHERE id_banda = '%s'" %idBanda
    c = auxMethods.getCursor(con)
    c.execute(query)
    id = None
    id = c.fetchone()[0]
    query = "DELETE FROM miembrobanda WHERE id_miembro = %s AND id_banda = %s"
    try:
        auxMethods.getCursor(con).execute(query, (token, idBanda))
        con.commit()
        con.close()
        data = "Has abandonado la banda" +idBanda
        ret = json.dumps(data)
        return ret
    except:
        con.close()
        data = "No se ha podido abandonar la banda"
        ret = json.dumps(data)
        return ret



if __name__=='__main__':
	app.run(debug=True, host="127.0.0.1")
