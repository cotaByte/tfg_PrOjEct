from re import X
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
        con = sqlite3.connect('myissues.db')
        return con
    except Error:
        print(Error)

@app.route('/greetings', methods=["GET"])
def greetings():
    if request.method == "GET":
        response = request.data
        array=json.loads(response.decode('utf-8'))
        token = array.get('token')
        email = auxMethods.getUserEmailFromid(token)
        name = auxMethods.getUserNameFromid(token)
        surname = auxMethods.getUserSurnameFromid(token)
        ret = json.dumps({'email':email, 'name':name, 'surname':surname})
        return ret

#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
@app.route('/login', methods =["GET", "POST"])
def login():
    
    if request.method == "POST":
        response = request.data
        array=json.loads(response.decode('utf-8'))
        
        ret = login(array.get('email'), array.get('password'))
        return ret
		
def login(email, pw):                                                           # Method for log a user  //////////////////////////DONE
    token = None
    con= connection()
    query = 'SELECT id, email, password, name FROM Users'
    for row in auxMethods.getCursor(con).execute(query):
        if(row[1] == email and row[2] == pw):
            token = row[0]
            ret = json.dumps(token)
            return ret
    con.close()
    ret = json.dumps(token)
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
@app.route('/addUser', methods =["POST"])
def registerUser():
    if(request.method=="POST"):
        response = request.data
        array=json.loads(response.decode('utf-8'))

        return addUser(array.get('name'),array.get('surname'), array.get('email'), array.get('password'))


def addUser(name, surname, email, pwd):                                     # Method for add a User to the database 
    con = connection()
    for row in auxMethods.getCursor(con).execute('SELECT email FROM Users'):
        if(row[0] == email):
            data =  "Email already exists"
            ret = json.dumps({'data':data, 'error':True})                                              # Check if the user already exists by using the email
            return ret
    id = str(round(time.time()*1000))
    query = 'INSERT INTO Users (id, name, surname, email, password) VALUES (%s, "%s", "%s", "%s", "%s")'%(id, name, surname, email, pwd)
    auxMethods.getCursor(con).execute(query)
    con.commit()
    con.close()
    data = "User added"
    ret = json.dumps({'data':data, 'error':False})                                              # Check if the user already exists by using the email
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////      DONE
@app.route('/listUsers', methods =["GET"])
def listUsers():
    if(request.method=="GET"):

        return listUsers()

def listUsers ():                                               
    con = connection()
    c = auxMethods.getCursor(con)
    c.execute('SELECT * FROM Users')
    data = c.fetchall()
    c.close()
    ret = json.dumps(data)
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/removeUser', methods =["DELETE", "GET"])
def removeUser():
    if(request.method=="DELETE"):
        id = request.args.get('id')

        rmUser(id)
        return ""


def rmUser (id):                                                         # Method to remove the user //////////////////////////DONE
    con = connection()
    query = "DELETE FROM Users WHERE id ="+str(id)
    query2 = "DELETE FROM UsersWS WHERE userId ="+str(id)
    query3 = "SELECT COUNT(*) FROM UsersWS WHERE userId ="+str(id)

    auxMethods.getCursor(con).execute(query)
    con.commit()
    c = auxMethods.getCursor(con).execute(query3)
    x = 0
    x = c.fetchone()[0]
    if(x > 0):                                                                  # Test if the user exists in the table WSUsers
        auxMethods.getCursor(con).execute(query2)
        con.commit()
    con.close()
    data = "The user was deleted"  
    ret = json.dumps(data)
    





#/////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/addWorkspace', methods =["POST"])
def wsAdder():
    if(request.method=="POST"):
        response = request.data
        array=json.loads(response.decode('utf-8'))
        return addWS(array.get('name'),array.get('description')) 

def addWS(name, des):                                                    # Method for add a User to the database //////////////////////////DONE
    con = connection()
    for row in auxMethods.getCursor(con).execute('SELECT name FROM WorkSpaces'):
        if(row[0] == name):                                                     #Check if the Workspace already exists by using the name
            data="The workSpace already exists"
            ret = json.dumps({'data':data, 'error':True})                                              # Check if the user already exists by using the email
            return ret

    id = str(round(time.time()*1000))
    query = 'INSERT INTO WorkSpaces (id, name, description) VALUES (%s, "%s","%s")'%(id, name, des)
    auxMethods.getCursor(con).execute(query)
    con.commit()
    con.close()
    data= "WorkSpace "+name+" added"
    ret = json.dumps({'data':data, 'error':False})                                              # Check if the user already exists by using the email
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listWorkspaces', methods =["GET"])
def listWorkspaces():
        if(request.method=="GET"):
            return listWS()

def listWS ():                                                          #Mehtod to list the Users //////////////////////////DONE
    con = connection()
    c = auxMethods.getCursor(con)
    c.execute('SELECT * FROM WorkSpaces')
    data = c.fetchall()
    c.close()
    ret = json.dumps(data)
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/removeWorkspace', methods =["DELETE", "GET"])
def removeWorkspace():
    if(request.method=="DELETE"):
        id = request.args.get('id')
        rmWS(id)
        return ""
    if(request.method=="GET"):
        return redirect("/listWorkspace")

def rmWS (id):                                                         # Method to remove the user //////////////////////////DONE
    con = connection()
    query = "DELETE FROM WorkSpaces WHERE id ="+str(id)
    query2 = "DELETE FROM UsersWS WHERE wsId ="+str(id)
    query3 = "SELECT COUNT(*) FROM UsersWS WHERE wsId ="+str(id)

    auxMethods.getCursor(con).execute(query)
    con.commit()
    c = auxMethods.getCursor(con).execute(query3)
    x = 0
    x = c.fetchone()[0]
    if(x > 0):                                                                  # Test if the user exists in the table WSUsers
        auxMethods.getCursor(con).execute(query2)
        con.commit()
    con.close()
    data = "The workspace was deleted"  
    ret = json.dumps(data)
#/////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listJoin',  methods =["GET", "POST"])
def  listWSJoin():
    if request.method=="GET":
        response = request.data
        array=json.loads(response.decode('utf-8'))
        token=array.get('token')
        return listJoin(token)

def listJoin(token):
    con = connection()
    c = auxMethods.getCursor(con)
    data=[]
    query= "SELECT  id FROM WorkSpaces"
    for row in auxMethods.getCursor(con).execute(query):
        query2=  "SELECT wsId FROM UsersWS WHERE wsId= ? AND userId=?"
        result= auxMethods.getCursor(con).execute(query2, (str(row[0]), str(token)))
        res= result.fetchone()
        if res is not None:                                                          #Problem with the fetchone (1354756576654, )
            res=res[0]
            data.append(res)
    placeholder= '?' # For SQLite.
    placeholders= ', '.join(placeholder for unused in data)
    if(len(data) == 0):
        query3= 'SELECT id, name, description FROM WorkSpaces'
        c.execute(query3)
    else:
        query3= 'SELECT id, name, description FROM WorkSpaces  WHERE id NOT IN ({})'.format(placeholders)
        c.execute(query3, data)

    data2=c.fetchall()
    c.close()
    ret=json.dumps(data2)
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/join', methods =["POST"])
def joinWS():
    if(request.method=="POST"):

        response = request.data
        array=json.loads(response.decode('utf-8'))
        id = array.get('wsId')
        token = array.get('token')
        ret = join(token, id)
        return ret

def join (token, wsid):                                                    # Method for join the user to a workspace //////////////////////////DONE
    con = connection()                                                          #Obtain Workspace id and name                                           
    query = "SELECT id,name FROM WorkSpaces WHERE id = '%s'" %wsid
    c = auxMethods.getCursor(con)
    c.execute(query)
    rows = c.fetchall()
    id = ""
    name = ""
    for row in rows:
        id = row[0]
        name = row[1]
    query2 = "SELECT userId, wsId FROM UsersWS WHERE userId = ? AND wsId = ?"
    c.execute(query2, (str(token), str(wsid)))                                     # Check if the user is in the workspace
    res = None
    res = c.fetchall()
    if (res):
        con.close()
        data = " The user is already in the workspace"
        ret = json.dumps(data)
        return ret
    if(int(wsid) == int(id)):     
        query3 = "INSERT INTO UsersWS (userId, wsId) VALUES ('%s','%s')" %((str(token),str(id)))
        auxMethods.getCursor(con).execute(query3)
        con.commit()
        con.close()
        data = "User joined to workspace "+name
        ret = json.dumps(data)
        return ret
    else:
        con.close()
        data = "Wrong workspace"
        ret = json.dumps(data)
        return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listLeave',  methods =["GET", "POST"])
def  listWSLeave():
    if request.method=="GET":
        response = request.data
        array=json.loads(response.decode('utf-8'))
        token=array.get('token')
        return listLeave(token)

def listLeave(token):
    con = connection()
    c = auxMethods.getCursor(con)
    data=[]
    query= "SELECT id FROM WorkSpaces"
    for row in auxMethods.getCursor(con).execute(query):
        query2 = "SELECT wsId FROM UsersWS WHERE wsId= ? AND userId=?"
        result= auxMethods.getCursor(con).execute(query2, (str(row[0]), str(token)))
        res= result.fetchone()
        if res is not None:                                                          #Problem with te fetchone (1354756576654, )
            res=res[0]
            data.append(res)
    placeholder= '?' # For SQLite. See DBAPI paramstyle.
    placeholders= ', '.join(placeholder for unused in data)
    query3= 'SELECT id, name, description FROM WorkSpaces  WHERE id IN ({})'.format(placeholders)
    c.execute(query3, data)
    data2=c.fetchall()
    c.close()
    ret=json.dumps(data2)
    return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
@app.route('/leave', methods =["POST"])
def leaveWS():
    if(request.method=="POST"):

        response = request.data
        array=json.loads(response.decode('utf-8'))
        id = array.get('wsId')
        token = array.get('token')
        ret = leave(token, id)
        return ret

def leave(token, wsid):                                                    # Method to leave the user a Workspace //////////////////////////DONE

    con = connection()
    query = "SELECT id FROM WorkSpaces WHERE id = '%s'" %wsid
    c = auxMethods.getCursor(con)
    c.execute(query)
    id = None
    id = c.fetchone()[0]

    query = "DELETE FROM UsersWS WHERE userId = ? AND wsId = ?"
    try:
        auxMethods.getCursor(con).execute(query, (int(token), int(id)))
        con.commit()
        con.close()
        data = "You leave " +str(wsid)+ " workspace"
        ret = json.dumps(data)
        return ret

    except:
        con.close()
        data = "The user couldn't leave WorkSpace"
        ret = json.dumps(data)
        return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/addIssue', methods =["POST"])
def issueAdder():
    if(request.method=="POST"):
        response = request.data
        array=json.loads(response.decode('utf-8'))
        return addIssue(array.get('token'),array.get('name'),array.get('workspace'))

def addIssue(token, issueName, workspaceName):                                  # Add a Issue to the table //////////////////////////DONE
    con = connection()                  
    idWS=auxMethods.getIdWS(workspaceName)                                                # Get the id of the workspace
    if(idWS == None):                                                          # If the id is none, the ws does not exist
        data= "The workspace does not exist"
        ret = json.dumps({'data':data, 'error':True})                                              # Check if the user already exists by using the email
        return ret
    if auxMethods.testAddIssueName(issueName)== False:
        data= "The issue already exists"
        ret = json.dumps({'data':data, 'error':True})                                              # Check if the user already exists by using the email
        return ret
    if auxMethods.checkUserInWS(idWS, token)==True :                                     # If the user is joined to the workspace, can be added
        creator= token                                                         # Assign the values
        state= 0
        assign= None 
        date= datetime.now()
        id = str(round(time.time()*1000))
        query= 'INSERT INTO Issues (id, name, creator, state, assigned, workspace,date) VALUES (%s, "%s", "%s", "%s", "%s",  "%s", "%s")'%(id, issueName, creator, state,  assign, idWS, date)
        c= auxMethods.getCursor(con)
        c.execute(query)
        con.commit()
        con.close()
        data= "Issue "+issueName+"  added"
        ret = json.dumps({'data':data, 'error':False})                                              # Check if the user already exists by using the email
        return ret
    else:
        data= "You do not belong to the workspace, join first "
        ret = json.dumps({'data':data, 'error':True})                                              # Check if the user already exists by using the email
        return ret
#/////////////////////////////////////////////////////////////////////////////////////////////////		DONE
@app.route('/listIssues', methods =["GET"])
def issueLister():
    if(request.method=="GET"):
        response = request.data
        array=json.loads(response.decode('utf-8'))
        token = array.get('token')
        type = array.get('type')
        return listIssues(token, type)

def listIssues (token, modality):                                             # Mehtod for List Issues based on the state of the Issue 
    con = connection()
    c = auxMethods.getCursor(con)
    arrayWS=[]
    arrayCreator=[]
    arrayAssigned=[]
    arrayStatus=[]
    if modality== "all":                                
        query = 'SELECT id,name,workspace, creator, assigned, state, date FROM Issues '
        c.execute(query)
        data=c.fetchall()       
        for row in data:
            #get WSName
            wsId= str(row[2])
            wsName = auxMethods.getWsNameFromid(wsId)
            arrayWS.append(wsName)
            
            #get Creator
            creatorId = str(row[3])
            creatorName = auxMethods.getUserNameFromid(creatorId)
            arrayCreator.append(creatorName)

            #get Assigned
            assignedId = str(row[4])
            assignedEmail = auxMethods.getUserEmailFromid(assignedId)
            arrayAssigned.append(assignedEmail)

            #get State
            state = str(row[5])
            status = auxMethods.convertState(state)
            arrayStatus.append(status)
        con.close()
        ret = json.dumps({'arrayWS': arrayWS, 'arrayCreator':arrayCreator, 'arrayAssigned':arrayAssigned, 'arrayStatus':arrayStatus, 'data': data})
        return ret
    elif modality== "created":
        query = 'SELECT id,name,workspace, creator, date FROM Issues WHERE state = 0'        
        c.execute(query)
        data=c.fetchall()
        for row in data:
            #get WSName
            wsId= str(row[2])
            wsName = auxMethods.getWsNameFromid(wsId)
            arrayWS.append(wsName)
            #get Creator
            creatorId = str(row[3])
            creatorName = auxMethods.getUserNameFromid(creatorId)
            arrayCreator.append(creatorName)
        con.close()
        ret = json.dumps({'arrayWS': arrayWS, 'arrayCreator':arrayCreator,'data':data})
        return ret
    elif modality== "notassigned":                                
        query = 'SELECT id,name,workspace, creator, date FROM Issues WHERE state = 1 '
        c.execute(query)
        data=c.fetchall()
        for row in data:
            #get WSName
            wsId= str(row[2])
            wsName = auxMethods.getWsNameFromid(wsId)
            arrayWS.append(wsName)
            
            #get Creator
            creatorId = str(row[3])
            creatorName = auxMethods.getUserNameFromid(creatorId)
            arrayCreator.append(creatorName)
        con.close()
        ret = json.dumps({'arrayWS': arrayWS, 'arrayCreator':arrayCreator,'data':data})
        return ret
    elif modality== "assigned":
        query = "SELECT id,name,workspace, creator, date FROM Issues WHERE state = 2 AND assigned = '%s'" %(str(token))
        c.execute(query)
        data=c.fetchall()
        for row in data:
            #get WSName
            wsId= str(row[2])
            wsName = auxMethods.getWsNameFromid(wsId)
            arrayWS.append(wsName)
            #get Creator
            creatorId = str(row[3])
            creatorName = auxMethods.getUserNameFromid(creatorId)
            arrayCreator.append(creatorName)
        con.close()
        ret = json.dumps({'arrayWS': arrayWS, 'arrayCreator':arrayCreator,'data':data})
        return ret
    elif modality== "accepted":
        query = "SELECT id,name,workspace, creator, date FROM Issues WHERE state = 3 AND assigned = '%s'" %(str(token))
        c.execute(query)
        data=c.fetchall()
        for row in data:
            #get WSName
            wsId= str(row[2])
            wsName = auxMethods.getWsNameFromid(wsId)
            arrayWS.append(wsName)
            #get Creator
            creatorId = str(row[3])
            creatorName = auxMethods.getUserNameFromid(creatorId)
            arrayCreator.append(creatorName)
        con.close()
        ret = json.dumps({'arrayWS': arrayWS, 'arrayCreator':arrayCreator,'data':data})
        return ret
    elif modality== "completed":
        query = "SELECT id,name,workspace, creator, date FROM Issues WHERE state = 4 "
        c.execute(query)
        data=c.fetchall()
        for row in data:
            #get WSName
            wsId= str(row[2])
            wsName = auxMethods.getWsNameFromid(wsId)
            arrayWS.append(wsName)
            #get Creator
            creatorId = str(row[3])
            creatorName = auxMethods.getUserNameFromid(creatorId)
            arrayCreator.append(creatorName)
        con.close()
        ret = json.dumps({'arrayWS': arrayWS, 'arrayCreator':arrayCreator,'data':data})
        return ret
    else :
        return ""
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__=='__main__':
	app.run(debug=True, host="0.0.0.0")
