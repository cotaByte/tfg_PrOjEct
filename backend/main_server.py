from _thread import *
import  Utilidades
from flask import Flask, request
from flask_cors import CORS
import Evento,Miembro,Banda,Require

# CORS: Permitirá recibir requests externas a una app flask.
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        dni = request.args.get('dni' )
        pwd = request.args.get('pwd')
        ret = Miembro.login(dni, pwd)
        return ret
# /////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/addMiembro', methods=["POST"])
def register_user():
    if (request.method == "POST"):
        dni = request.args.get('dni')
        nombre = request.args.get('nombre')
        apellido1 = request.args.get('apellido1')
        apellido2 = request.args.get('apellido2')
        instrumento = request.args.get('instrumento')
        director = True if request.args.get('director')=='true' else False
        tlf = request.args.get('telefono')
        pwd = request.args.get('pwd')
        return Miembro.add_user(dni, nombre, apellido1, apellido2, instrumento, director,tlf, pwd)
# /////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/addBanda', methods=["POST"])
def register_banda():
    if (request.method == "POST"):
        nombre = request.args.get('nombre')
        poblacion = request.args.get('poblacion')
        return Banda.add_banda(nombre, poblacion)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listMiembros', methods=['GET', 'HEAD'])
def get_miembros():
    if (request.method == 'GET'):
        id = request.args.get('id_miembro')
        return Miembro.list_miembros(id)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listBandas',    methods=['GET', 'HEAD'])
def get_bandas():
    if (request.method == 'GET'):
        return Banda.list_bandas()
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/join', methods=["POST"])
def join_banda():
    if (request.method == "POST"):
        token = request.args.get('token')
        id_banda = request.args.get('id_banda')
        ret = Banda.join(token,id_banda)
        return ret
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listJoin', methods=["GET"])
def join_lister():
    if (request.method == "GET"):
        token = request.args.get('token')
        return Banda.list_join(token)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listLeave', methods=["GET"])
def leave_lister():
    if (request.method == "GET"):
        token = request.args.get('token')
        return Banda.list_leave(token)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/leave', methods=["POST"])
def leave_banda():
    if (request.method == "POST"):
        token = request.args.get('token')
        id_banda = request.args.get('id_banda')
        return Banda.leave(token, id_banda)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/addEvento', methods=['POST'])
def event_register():
    if (request.method == 'POST'):
        nombre = request.args.get('nombre')
        ubicacion = request.args.get('ubicacion')
        fecha_evento = request.args.get('fecha_evento')
        estado = 0  # only created
        return Evento.register_event(nombre, ubicacion, fecha_evento, estado)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listEventos', methods=['GET', 'HEAD'])
def get_events():
    if (request.method == 'GET'):
        return Evento.list_events()
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/removeMiembro', methods=['DELETE', 'GET'])
def remove_member():
    if (request.method == "DELETE"):
        id_miembro = request.args.get('id_miembro')
        return Miembro.rm_member(id_miembro)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/removeBanda', methods=['DELETE', 'GET'])
def remove_banda():
    if (request.method == "DELETE"):
        id_banda = request.args.get('id_banda')
        return Banda.rm_banda(id_banda)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/removeEvent', methods=['DELETE'])
def remove_event():
    if (request.method == "DELETE"):
        id_evento = request.args.get('id')
        return Evento.rm_evento(id_evento)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/addEventoRequerimiento',   methods=['POST'])
def register_requirement():
    # recibimos el numero max de   instrumentos, el instrumento , el id_evento  al que esta asociado
    if (request.method == 'POST' ):
        id_evento = request.args.get('id_evento')
        instrumento = request.args.get("id_instrumento")
        num_max = request.args.get("num_max")
        return Require.insert_requirement(id_evento, instrumento, num_max)  
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/listRequirementsForEvent', methods=['GET', 'HEAD'])
def get_requirements_for_event():
    if (request.method == 'GET'):
        id_evento = request.args.get('id_evento')
        id_miembro= request.args.get ('id_miembro')
        return Require.list_requirements_for_event(id_miembro,id_evento)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/inscribeToEvent',  methods=['POST'])
def add_subscribe_to_an_event():
    if (request.method == 'POST'):
        id_miembro = request.args.get("id_miembro")
        id_evento = request.args.get("id_evento")
        id_require = request.args.get("id_requerimiento")
        return  Evento.inscribe_to_an_event( id_miembro, id_require, id_evento)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/closeEvent', methods=['POST'])
def event_closer():
    if (request.method == 'POST'):
        print(request.args)
        id_evento = request.args.get('id_evento')
        return Evento.close_event(id_evento)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/checkToken' , methods=['GET'])
def token_checker():
    if (request.method=='GET'):
        token = request.args.get('id_miembro')
        return Utilidades.check_token(token)
# aqui iba antes el checkToken
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/removeRequerimiento' , methods=['DELETE'])
def requirement_rm():
    if (request.method=='POST'):
        id_req = request.args.get('id_requerimiento')
        return Require.remove_requerimiento(id_req)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/desInscribeForEvent' , methods=['DELETE'])
def event_desinscriber():
    if (request.method=='DELETE'):
        id_req = request.args.get('id_requerimiento')
        token = request.args.get('id_miembro')
        return Evento.desinscribe_for_event(id_req, token)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/getEventosByMiembro', methods=['GET'])
def get_eventos_by_miembro():
    if (request.method=='GET'):
        token = request.args.get('id_miembro')
        return Evento.get_eventos_by_miembro(token)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if  __name__ == '__main__':
    #app.run(debug=True, host="127.0.0.1", ssl_context = 'adhoc') => Parametro para utilizar https:// Need certifcate
    app.run(debug=True, host="127.0.0.1")
    #app.run(debug=True, host="172.20.0.3") para despliegue en prod
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
