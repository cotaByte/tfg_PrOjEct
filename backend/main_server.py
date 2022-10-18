from crypt import methods
from ctypes.wintypes import PINT
from re import T, X
import psycopg2
import time
import json
from _thread import *
import auxMethods
from flask import Flask, request, redirect
from flask_cors import CORS

app = Flask(__name__)
# CORS: Permitirá recibir requests externas a una app flask.
cors = CORS(app, resources={r"/*": {"origins": "*"}})
host = "localhost"  # aqui podriamos cambiar la direccion ip en la que se encuentre la BD


def connection():  # metodo para conectarse a la base de datos
    try:
        con = psycopg2.connect(
            host=host,
            user='postgres',
            password='password',
            database='xarangapp'
        )
        return con
    except Exception as ex:
        print(ex)
# /////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/greetings', methods=["GET"])
def greetings():
    if request.method == "GET":
        response = request.data
        array = json.loads(response.decode('utf-8'))
        token = array.get('token')
        nombre = auxMethods.getUserNameFromid(token)
        apellido1 = auxMethods.getUserSurname1Fromid(token)
        apellido2 = auxMethods.getUserSurname2Fromid(token)
        ret = json.dumps(
            {'nombre': nombre, 'apellido1': apellido1, 'apellido2': apellido2})
        return ret
# /////////////////////////////////////////////////////////////////////////////////////////////////		 DONE


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        """ 
        Forma  vieja de realizar el decode del json recibido por el json
        response = request.data
        array=json.loads(response.decode('utf-8'))
        nif= array.get('nif')
        pin= array.get('pin')  """
        nif = request.args.get('nif')
        pin = request.args.get('pin')
        ret = login(nif, pin)
        return ret


def login(nif, pin):  # Method to log in on de website
    token = None
    con = connection()
    query = 'SELECT id, nif, pin, nombre FROM Miembros'
    c = auxMethods.getCursor(con)
    c.execute(query)
    for record in c:
        if (record['nif'] == int(nif) and str(record['pin']) == str(pin)):
            token = record['id']
            ret = json.dumps(token)
            # with the return here, the loop stops when it smash the match (no innecesary iterations)
            return ret
    con.close()
    ret = json.dumps(token)
    return ret
# /////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/addMiembro', methods=["POST"])
def registerUser():
    if (request.method == "POST"):
        """ response = request.data
        array=json.loads(response.decode('utf-8'))
        nif= array.get('nif')
        nombre=array.get('nombre') 
        apellido1=array.get('apellido1')
        apellido2=array.get('apellido2')
        instrumento=array.get('instrumento')    
        director = array.get('director')
        banda = array.get('banda')
        tlf=  array.get('tlf')"""
        nif = request.args.get('nif')
        nombre = request.args.get('nombre')
        apellido1 = request.args.get('apellido1')
        apellido2 = request.args.get('apellido2')
        instrumento = request.args.get('instrumento')
        director = request.args.get('director')
        banda = request.args.get('banda')
        tlf = request.args.get('tlf')
        pin = request.args.get('pin')

        return addUser(nif, nombre, apellido1, apellido2, instrumento, director, banda, tlf, pin)


# Method for add a User to the database
def addUser(nif, nombre, apellido1, apellido2, instrumento, director, banda, tlf, pin):
    con = connection()
    c = auxMethods.getCursor(con)
    query = 'SELECT nif FROM Miembros'
    c.execute(query)
    for record in c:
        if (record['nif'] == nif):
            data = "El usuario ya existe"
            con.close()
            # Check if the user already exists by using the email
            ret = json.dumps({'data': data, 'ok': False})
            return ret

    def id(a): return str(round(time.time()*1000)
                          ) if director == 0 else str(round(time.time()*1000))+"D"
    # Get timestamp for the id of the user
    c.execute('INSERT INTO Miembros (id, nif, nombre, apellido1, apellido2, id_instrumento, telefono, id_banda, director, pin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)', (id(
        director), int(nif), nombre, apellido1, apellido2, int(instrumento), int(tlf), banda, director, int(pin)))
    con.commit()
    con.close()
    data = "Miembro añadido correctamente"
    # Check if the user already exists by using the email
    ret = json.dumps({'data': data, 'ok': True})
    return ret
# /////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/addBanda', methods=["POST"])
def registerBanda():
    if (request.method == "POST"):
        """ response= request.data
        array=json.loads(response.decode('utf-8'))
        nombre= array.get('nombre')
        poblacion = array.get('poblacion') """
        nombre = request.args.get('nombre')
        poblacion = request.args.get('poblacion')
        return addBanda(nombre, poblacion)


def addBanda(nombre, poblacion):
    con = connection()
    c = auxMethods.getCursor(con)
    query = 'SELECT nombre FROM Bandas'
    c.execute(query)
    for record in c:
        if (record['nombre'] == nombre):
            data = "Esta banda ya se encuentra registrada"
            con.close()
            # Check if the user already exists by using the email
            ret = json.dumps({'data': data, 'ok': False})
            return ret

    id = str(round(time.time()*1000))
    c.execute('INSERT INTO Bandas (id_banda, nombre, poblacion) VALUES (%s, %s, %s) ',
              (id, nombre, poblacion))
    con.commit()
    con.close()
    data = "Banda añadida correctamente"
    # Check if the user already exists by using the email
    ret = json.dumps({'data': data, 'ok': True})
    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/listMiembros', methods=['GET', 'HEAD'])
def getUsers():
    if (request.method == 'GET'):
        return listMembers()


def listMembers():
    con = connection()
    c = auxMethods.getCursor(con)
    c.execute(
        "SELECT id, nombre, apellido1, apellido2,id_instrumento, telefono FROM Miembros")
    data = c.fetchall()
    c.close()
    ret = json.dumps(data)
    print(ret)
    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/listBandas', methods=['GET', 'HEAD'])
def getBandas():
    if (request.method == 'GET'):
        return listBandas()


def listBandas():
    con = connection()
    c = auxMethods.getCursor(con)
    c.execute("SELECT * FROM Bandas")
    data = c.fetchall()
    c.close()
    ret = json.dumps(data)

    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/join', methods=["POST"])
def joinBanda():
    if (request.method == "POST"):
        """   response = request.data
        array=json.loads(response.decode('utf-8'))
        idBanda = array.get('id')
        token = array.get('token') """
        token = request.args.get('token')
        idBanda = request.args.get('id')
        ret = join(token, idBanda)
        return ret


def join(token,  idBanda):
    con = connection()
    c = auxMethods.getCursor(con)
    sql = "SELECT nombre FROM Bandas WHERE id_banda = '%s' " % idBanda
    c.execute(sql)
    for record in c:
        name = record['nombre']
        c.execute(
            "SELECT id_miembro, id_banda FROM miembro_banda WHERE id_miembro =%s AND id_banda = %s  ", (token, idBanda))
        res = None
        res = c.fetchall()
        if (res):
            con.close()
            data = "El miembro ya se encuentra en esta banda"
            ret = json.dumps(data)
            return ret
        try:
            sqlInsert = "INSERT INTO miembro_banda (id_miembro,id_banda) VALUES (%s,%s )"
            c.execute(sqlInsert, (token, idBanda))
            con.commit()
            data = "Te has añadido a la banda  "+name+" correctamente"
            con.close()
            ret = json.dumps(data)
            return ret
        except:
            con.close()
            data = "Hubo un error al intentar unirse a esta banda"
            ret = json.dumps(data)
            return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/listJoin', methods=["GET"])
def joinLister():
    if (request.method == "GET"):
        """ response= request.data
        array = json.loads(response.decode('utf-8'))
        token = array.get("token") """
        token = request.args.get('token')
        return listJoin(token)


def listJoin(token):
    con = connection()
    c = auxMethods.getCursor(con)
    sql = " select * from Bandas where id_banda not in (select id_banda from miembro_banda where id_miembro= %s );"
    c.execute(sql, (token,))
    data = c.fetchall()
    c.close()
    ret = json.dumps(data)
    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/listLeave', methods=["GET"])
def leaveLister():
    if (request.method == "GET"):
        """ response= request.data
        array = json.loads(response.decode('utf-8'))
        token = array.get("token") """
        token = request.args.get('token')
        return listLeave(token)


def listLeave(token):
    con = connection()
    c = auxMethods.getCursor(con)
    sql = " select * from Bandas where id_banda in (select id_banda from miembro_banda where id_miembro= %s );"
    c.execute(sql, (token,))
    data = c.fetchall()
    c.close()
    ret = json.dumps(data)
    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/leave', methods=["POST"])
def leaveBanda():
    if (request.method == "POST"):
        """ response= request.data6
        array = json.loads(response.decode('utf-8'))
        idBanda = array.get ("id")
        token = array.get ("token") """
        token = request.args.get('token')
        idBanda = request.args.get('id')
        ret = leave(token, idBanda)
        return ret


def leave(token, idBanda):
    con = connection()
    c = auxMethods.getCursor(con)
    query = "DELETE FROM miembro_banda WHERE id_miembro = %s AND id_banda = %s"
    try:
        auxMethods.getCursor(con).execute(query, (token, idBanda))
        con.commit()
        con.close()
        data = "Has abandonado la banda" + idBanda
        ret = json.dumps(data)
        return ret
    except:
        con.close()
        data = "No se ha podido abandonar la banda"
        ret = json.dumps(data)
        return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/addEvent', methods=['POST'])
def eventRegister():
    if (request.method == 'POST'):
        """ response= request.data
        array = json.loads(response.decode('utf-8'))
        nombre = array.get ("nombre")
        ubicacion = array.get("ubicacion")
        fecha_evento= array.get("fecha_evento") """
        nombre = request.args.get('nombre')
        ubicacion = request.args.get('ubicacion')
        fecha_evento = request.args.get('fecha_evento')
        estado = 0  # only created

        return registerEvent(nombre, ubicacion, fecha_evento, estado)


def registerEvent(nombre, ubicacion, fecha_evento, estado):
    con = connection()
    c = auxMethods.getCursor(con)
    sql = "SELECT nombre FROM eventos WHERE nombre = '%s'" % nombre
    c.execute(sql)
    if (c.rowcount != 0):
        con.close()
        data = "Ya existe un evento registrado con este codigo"
        # Check if the event is already registered
        ret = json.dumps({'data': data, 'ok': False})
        return ret

    id = str(round(time.time()*1000))
    c.execute('INSERT INTO eventos (id_evento, nombre, ubicacion,fecha_evento,estado) VALUES (%s, %s, %s,%s,%s) ',
              (id, nombre, ubicacion, fecha_evento, estado))
    con.commit()
    con.close()
    data = "Evento añadido correctamente"
    ret = json.dumps({'data': data, 'ok': True})
    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/listEvents', methods=['GET', 'HEAD'])
def getEvents():
    if (request.method == 'GET'):
        return listEvents()


def listEvents():
    con = connection()
    c = auxMethods.getCursor(con)
    c.execute("SELECT * FROM Eventos")
    data = c.fetchall()
    c.close()
    ret = json.dumps(data)
    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/listInstrumentos', methods=['GET', 'HEAD'])
def getInstrumentos():
    if (request.method == 'GET'):
        return listInstrumentos()


def listInstrumentos():
    con = connection()
    c = auxMethods.getCursor(con)
    c.execute("SELECT * FROM Instrumentos")
    data = c.fetchall()
    c.close()
    ret = json.dumps(data)
    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/removeMiembro', methods=['DELETE', 'GET'])
def removeMember():
    if (request.method == "DELETE"):
        id_miembro = request.args.get('id')
        return rmMember(id_miembro)
    if (request.method == "GET"):
        return redirect("/listMembers")


# Method to remove the user //////////////////////////DONE
def rmMember(id):
    con = connection()
    sql = "DELETE FROM Miembros WHERE id ='"+str(id)+"'"
    sql2 = "DELETE FROM miembro_banda WHERE id_miembro ='"+str(id)+"'"

    try:
        c = auxMethods.getCursor(con)
        c.execute(sql)
        c.execute(sql2)
        con.commit()
        con.close()
        data = "El miembro fue eliminado correctamente"
        ret = json.dumps(data)
        return ret
    except:
        data = "Hubo un error al tratar de eliminar el miembro"
        ret = json.dumps(data)
        return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/removeBanda', methods=['DELETE', 'GET'])
def removeBanda():
    if (request.method == "DELETE"):
        id_banda = request.args.get('id')
        return rmBanda(id_banda)
    if (request.method == "GET"):
        return redirect("/listBandas")


def rmBanda(id):
    con = connection()
    sql = "DELETE FROM Bandas WHERE id_banda ='"+str(id)+"'"
    sql2 = "DELETE FROM miembro_banda WHERE id_banda ='"+str(id)+"'"
    try:
        c = auxMethods.getCursor(con)
        c.execute(sql)
        c.execute(sql2)
        con.commit()
        con.close()
        data = "La banda fue eliminada correctamente"
        ret = json.dumps(data)
        return ret
    except:
        data = "Hubo un error al tratar de eliminar la banda"
        ret = json.dumps(data)
        return ret

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/removeEvent', methods=['DELETE', 'GET'])
def removeEvent():
    if (request.method == "DELETE"):
        id_evento = request.args.get('id')
        return rmEvento(id_evento)
    if (request.method == "GET"):
        return redirect("/listEvents")


def rmEvento(id):
    con = connection()
    sql = "DELETE FROM Eventos WHERE id_evento ='"+str(id)+"'"
    try:
        c = auxMethods.getCursor(con)
        c.execute(sql)
        con.commit()
        con.close()
        data = "El evento fue eliminado correctamente"
        ret = json.dumps(data)
        return ret
    except:
        data = "Hubo un error al tratar de eliminar el evento"
        ret = json.dumps(data)
        return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/addEventRequirement',   methods=['POST'])
def registerRequirement():
    # recibimos el numero max de   instrumentos, el instrumento , el id_evento  al que esta asociado
    if (request.method == 'POST'):

        id_evento = request.args.get('id_evento')
        instrumento = request.args.get("id_instrumento")
        num_max = request.args.get("num_max")
        return insertRequirement(id_evento, instrumento, num_max)


def insertRequirement(id_evento, instrumento, num_max):

    con = connection()
    c = auxMethods.getCursor(con)
    sql = "select * from requerimientos_evento where id_evento  ='" + \
        str(id_evento)+"' and id_instrumento   ='"+str(instrumento)+"'"
    c.execute(sql)
    if (c.rowcount != 0):
        con.close()
        data = "Ya existe un require registrado con este codigo"
        ret = json.dumps({'data': data, 'ok': False})
        return ret
    id = str(round(time.time()*1000))
    sqlInsert = "INSERT INTO requerimientos_evento (id_require, id_evento,id_instrumento,max) values (%s,%s,%s,%s)"
    c.execute(sqlInsert, (id, id_evento, instrumento, num_max))
    con.commit()
    con.close()
    data = "El require se ha insertado  correctamente"
    ret = json.dumps({'data': data, 'ok': True})
    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/listRequirementsForEvent', methods=['GET', 'HEAD'])
def getRequirementsForEvent():
    if (request.method == 'GET'):
        id_evento = request.args.get('id_evento')
        return listRequirementsForEvent(id_evento)


def listRequirementsForEvent(id_evento):
    con = connection()
    c = auxMethods.getCursor(con)
    sql = "select * from requerimientos_evento where id_evento  ='" + \
        str(id_evento)+"'"
    c.execute(sql)
    data = c.fetchall()
    c.close()
    ret = json.dumps(data)
    return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/inscribeToEvent', methods=['POST'])
def addSubscribeToAnEvent():
    if (request.method == 'POST'):
        id_evento = request.args.get('id_evento')
        instrumento = request.args.get("id_instrumento")
        id_miembro = request.args.get("id_miembro")
        return inscribeToAnEvent(id_evento, instrumento, id_miembro)


def inscribeToAnEvent(id_evento, instrumento, id_miembro):
    con = connection()
    c = auxMethods.getCursor(con)
    sql = "SELECT * FROM Eventos WHERE id_evento =  '"+str(id_evento)+"'"
    ret = ""
    data = "Has sido reescrito en el evento correctamente"
    c.execute(sql)
    if (c.rowcount == 0):
        con.close()
        data = "No existe un evento registrado con este  codigo"
        ret = json.dumps({'data': data, 'ok': False})
        return ret
    sql = "SELECT * FROM eventos_miembro_inscritos where id_instrumento = '" + \
        str(instrumento)+"' and id_evento = '"+str(id_evento)+"'"
    c.execute(sql)
    if (c.rowcount != 0):
        con.close()
        data = "Ya estas inscrito en este evento"
        ret = json.dumps({'data': data, 'ok': False})
        return ret
    sql = "SELECT actual,max from requerimientos_evento where id_instrumento = '" + \
        str(instrumento)+"' and id_evento = '"+str(id_evento)+"'"
    c.execute(sql)
    ret = c.fetchall()
    max = ret[0]['max']
    actual = ret[0]['actual']
    print(actual)
    print(max)
    if (actual == max):
        con.close()
        data = "El requerimiento para este evento respecto a este instrumento está ya completo"
        ret = json.dumps({'data': data, 'ok': False})
        return ret
    sql = "SELECT * FROM Miembros WHERE nif =  '" + \
        str(id_miembro)+"' and id_instrumento = '"+str(instrumento)+"'"
    c.execute(sql)
    if (c.rowcount == 0):
        con.close()
        data = "El usuario no tiene asignado este instrumento"
        ret = json.dumps({'data': data, 'ok': False})
        return ret
    sqlInsert = "INSERT INTO  eventos_miembro_inscritos (id_evento, id_miembro,id_instrumento) VALUES    (%s,%s,%s)"
    c.execute(sqlInsert, (id_evento, id_miembro, instrumento))
    actual = actual+1
    sqlUpdate = "UPDATE requerimientos_evento SET ACTUAL  ='" + \
        str(actual)+"'where id_instrumento = '"+str(instrumento) + \
        "' and id_evento = '"+str(id_evento)+"'"
    c.execute(sqlUpdate)
    con.commit()
    con.close()
    ret = json.dumps({'data': data, 'ok': False})
    return ret


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    #app.run(debug=True, host="127.0.0.1", ssl_context = 'adhoc')
    app.run(debug=True, host="127.0.0.1")
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
