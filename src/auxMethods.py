from datetime import date
from os import strerror
import socket,sqlite3,time,json,sys,threading, os, signal
from _thread import *
from sqlite3.dbapi2 import Connection, Date
from sqlite3 import Error
from datetime import datetime



def getCursor(con):                                                         # Method for create the object 4 the queries//////////////////////////DONE
    cursorObj = con.cursor()
    return cursorObj

def setConnection():
    try:
        con = sqlite3.connect('database.db')
        return con
    except Error:
        print(Error)


def getState(issueName):
    issueid = getIssueId(issueName)
    con = setConnection()
    q = "SELECT state FROM Issues WHERE id = '%s'" %(str(issueid))
    c= getCursor(con)
    c.execute(q)
    state = c.fetchone()
    if state is not None:                                                          #Problem with te fetchone (1354756576654, )
        state=state[0]                                                               #Fixed
    con.close()

    if state == None:
        return None
    else:
        return int(state)
    
def convertState(n):
    if(n=="0"):
        return "Created"
    if(n=="1"):
        return "Proposed"
    if(n=="2"):
        return "Assigned"
    if(n=="3"):
        return "Accepted"
    if(n=="4"):
        return "Completed"               


def checkUserInWS (wsid, userid):                                               # Check if the user is in the workspace //////////////////////////DONE

    con = setConnection()
    q0= "SELECT COUNT(*) FROM UsersWS WHERE userId = ? AND wsId = ? "
    c= getCursor(con)
    id =getIdWS(wsid)
    c.execute(q0, (str(userid), str(id)))
    test= c.fetchone()[0]
    con.close()
    if test == "0":                                                             # There user does not belong to the workspace
        return False
    else:
        return True



def getIdWS (WSName):                                                           # Get the id of the workspace //////////////////////////DONE
    con= setConnection()
    query= "SELECT id FROM WorkSpaces WHERE name= '%s'"  %(WSName)
    c= getCursor(con)
    c.execute(query)
    id= c.fetchone()
    if id is not None:                                                          #Problem with te fetchone (1354756576654, )
        id=id[0]                                                                #Fixed
    con.close()
    if id== None :
        return None
    else:
        return id



def getWsIdFromIssues(issueName):                                               #  Get the workspaceID from the Issues table /////////////////DONE
    con= setConnection()
    query= "SELECT workspace FROM Issues WHERE name= '%s'"  %(issueName)
    c= getCursor(con)
    c.execute(query)
    id= c.fetchone()
    if id is not None:
        id=id[0]
    con.close()
    if id== None :
        return None
    else:
        return id

def getIssueId(issueName):                                                      # Get the id of the Issue ///////////////////////////DONE
    con= setConnection()
    query= "SELECT id FROM Issues WHERE name= '%s'"  %(issueName)
    c= getCursor(con)
    c.execute(query)
    id= c.fetchone()
    if id is not None:
        id=id[0]
    con.close()
    if id== None :
        return None
    else:
        return id

def getIssueName(issueid):                                                      # Get the id of the Issue ///////////////////////////DONE
    con= setConnection()
    query= "SELECT name FROM Issues WHERE id= '%s'"  %(str(issueid))
    c= getCursor(con)
    c.execute(query)
    name= c.fetchone()
    if name is not None:
        name=name[0]
    con.close()
    if name== None :
        return None
    else:
        return name


def getIdFromEmail(email):                                                      # get the id of the user by his email
    con = setConnection()
    query= "SELECT id FROM Users WHERE email= '%s'" %(email)
    c = getCursor(con)
    c.execute(query)
    userid = c.fetchone()
    if userid is not None:
        userid = userid[0]
    con.close()
    if(userid  == None):
        return None
    else:
        return userid


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
    
