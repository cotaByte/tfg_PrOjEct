from datetime import date
import imp
from os import strerror
from _thread import *
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


""" 
def getCursor(conn):  # method for getting the cursor 
    cursorObj = conn.cursor()
    return cursorObj
 """




def getCursor(conn):  # method for getting the cursor 
    cursorObj = conn.cursor(cursor_factory = RealDictCursor)
    return cursorObj 



def setConnection(): # method for connecting to the database
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

def getUserNameFromid(id):                                                      # get the id of the user by his email
    con = setConnection()
    query= "SELECT nombre FROM Miembro WHERE id= '%s'" %(id)
    c = getCursor(con)
    c.execute(query)
    nombre = c.fetchone()
    if nombre is not None:
        nombre = nombre['nombre']
    con.close()
    if(nombre  == None):
        return None
    else:
        return nombre

def getUserSurname1Fromid(id):                                                      # get the id of the user by his email
    con = setConnection()
    query= "SELECT apellido1 FROM Miembro WHERE id= '%s'" %(id)
    c = getCursor(con)
    c.execute(query)
    apellido1 = c.fetchone()
    if apellido1 is not None:
        apellido1 = apellido1['apellido1']
    con.close()
    if(apellido1  == None):
        return None
    else:
        return apellido1

def getUserSurname2Fromid(id):                                                      # get the id of the user by his email
    con = setConnection()
    query= "SELECT apellido2 FROM Miembro WHERE id= '%s'" %(id)
    c = getCursor(con)
    c.execute(query)
    apellido2 = c.fetchone()
    if apellido2 is not None:
        apellido2 = apellido2['apellido2']
    con.close()
    if(apellido2  == None):
        return None
    else:
        return apellido2


def setObject4Server (form,*args) :
 # for each parameter passed to the function, get the element and  compound the dict (JSON) data to pass 2  the server
    data = {}
    for n in args:
        data [ n ]= form.get(n)
    print (data)
    return data
