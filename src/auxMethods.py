from datetime import date
from os import strerror
from _thread import *
import psycopg2
from datetime import datetime



def getCursor(conn):  # method for getting the cursor 
    cursorObj = conn.cursor()
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
        nombre = nombre[0]
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
        apellido1 = apellido1[0]
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
        apellido2 = apellido2[0]
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


""" 
def getUserEmailFromid(id):                                                      # get the id of the user by his email
    con = setConnection()
    query= "SELECT email FROM Users WHERE id= '%s'" %(id)
    c = getCursor(con)
    c.execute(query)
    name = c.fetchone()
    if name is not None:
        name = name[0]
    con.close()
    if(name  == None):
        return None
    else:
        return name

def getWsNameFromid(id):                                                      # get the id of the user by his email
    con = setConnection()
    query= "SELECT name FROM WorkSpaces WHERE id= '%s'" %(id)
    c = getCursor(con)
    c.execute(query)
    name = c.fetchone()
    if name is not None:
        name = name[0]
    con.close()
    if(name  == None):
        return None
    else:
        return name


def testAddIssueName(issueName):
    con = setConnection()
    query= "SELECT * FROM Issues WHERE name= '%s'" %(issueName)
    c = getCursor(con)
    c.execute(query)
    name = c.fetchone()
    
    if name is not None:
        return False
    con.close()
    if(name  == None):
        return True
    



def insertAction(t,creator,content,assigned ,issue):                            #insert an action to the database
    con = setConnection()
    date= datetime.now()
    params= (str (t), str(creator),str(content),str(assigned),str(issue), str(date))
    query2= 'INSERT INTO Actions (type, creator, content, assigned, issue, date) VALUES (?,?,?,?,?,?)'
    d= getCursor(con)
    d.execute(query2,params)
    con.commit()
    con.close()
    return "The action "+t+ " has been assigned successfully"

def registerHistory(action,issueName,created,assigned,date):                    #add a register to the history of an issue

    data = " "
    if action == 'propose':
        data = f'''The issue {issueName} was proposed by {created} at {date} \n'''
    elif action == 'reject':
        data = f'''The issue {issueName} was rejected by {created} at {date} \n'''
    elif action == 'comment':
        data = f'''The issue {issueName} was commented by {created} at {date} \n'''
    elif action == 'complete':
        data = f'''The issue {issueName} was completed by {created} at {date} \n'''
    elif action == 'acceptFinish' or action== 'accept':
        data = f'''The issue {issueName} was accepted by {created} at {date} \n'''
    elif action == 'assignFinish' or action == 'assign':
        data = f'''The issue {issueName} was assinged to {assigned} by {created} at {date} \n'''
    elif action == 'update':
        data = f'''The issue {issueName} was updated by {created} at {date} \n'''
    
    return data
     """
