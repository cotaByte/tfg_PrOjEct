import json
from datetime import date
from os import strerror
from _thread import *
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import hashlib

def get_cursor(conn):
    """Metodo que devuelve un cursor apuntando a la base de datos
    Args:
        conn (object): Conexión de la base de datos
    Returns:
        cursor: devuelve el cursor
    """
    cursor_obj= conn.cursor(cursor_factory=RealDictCursor)
    return cursor_obj


def set_connection():  
    """Crear una conexion a la base de datos
    Returns:
        Object: objeto de conexion a la BD
    """
    try:
        con = psycopg2.connect(

            #host='localhost',
            host='172.20.0.4', #para despliegue en prod
            user='postgres',
            password='password',
            database='xarangapp'
        )
        return con
    except Exception as ex:
        print(ex)


def get_full_nombre_miembro(token):
    """Funcion para devolver el nombre completo del miembro
    Args:
        token (string): id del miembro
    Returns:
        string: composicion de nombre y apellidos del  miembro
    """
    con = set_connection()
    query = "SELECT nombre, apellido1, apellido2 FROM Miembros WHERE id= '%s'" % (token)
    c = get_cursor(con)
    c.execute(query)
    nombre = c.fetchone()
    if (c.rowcount== 0):
        return None
    nombre_completo = nombre ['nombre'].capitalize() + " "+ nombre ['apellido1'].capitalize() + " "+ nombre ['apellido2'].capitalize()
    con.close()
    return nombre_completo


def get_miembro_instrumento(token):
    """Devuelve el instrumento asignado al miembro
    Args:
        token (string): id del miembro
    Returns:
        int : id de instrumento 
    """
    con = set_connection()
    sql = f"SELECT id_instrumento FROM Miembros where id ='{token}'"
    c= get_cursor(con)
    c.execute(sql)
    if (c.rowcount!=0):
        instrumento = c.fetchone()
        instrumento = instrumento['id_instrumento']
        con.close()
    return None if instrumento is None else  instrumento

def get_evento_require(id_require):
    """Devuelve el evento al que pertenece el require
    Args:
        id_require (string): id_require
    Returns:
        string: id del evento
    """
    con = set_connection()
    c= get_cursor(con)
    sql= f"select id_evento from requerimientos_evento where id_require = '{id_require}'"
    c.execute(sql)
    if (c.rowcount!=0):
        res = c.fetchone()
        id_evento = res['id_evento']
    con.close()
    return None if id_evento is None else  id_evento


def check_evento_exists(id_evento):
    """Comprueba si existe el evento
    Args:
        id_evento (string)
    Returns:
        Boolean
    """
    con = set_connection()
    c= get_cursor(con)
    sql= f"select * from eventos where id_evento = '{id_evento}'"
    c.execute(sql)
    con.close()
    return  False if c.rowcount==0 else True



def esta_miembro_inscrito_en_evento(id_miembro,id_evento):
    """Comprueba si el miembro esta inscrito en el evento
    Args:
        id_miembro (string)
        id_evento (string)
    Returns:
        Boolean
    """
    con= set_connection()
    c=get_cursor(con)
    if (check_token(id_miembro)==False):
     return False
    else:
        sql = f"select * from eventos_miembro_inscritos where id_evento= '{id_evento}' and id_miembro='{id_miembro}'"
        c.execute(sql)
        con.close()
        return  False if c.rowcount==0 else True

    
def check_token (token):
    """Comprueba el token y que el usuario exista
    Args:
        token (string)
    Returns:
        json: Objeto JSON con la comprobación
    """
    if (len(token)<10):
        msg= 'La longitud del token no es correcta'
        valid= False
        ret = json.dumps({'msg': msg , 'valid':valid})
        return ret 
    con =set_connection()
    c = get_cursor(con)
    sql = f"SELECT * FROM Miembros where id = '{token}'"
    c.execute(sql)
    if (c.rowcount!=0):
        msg= 'El usuario existe'
        valid= True
    else:
        msg= 'El usuario no  existe'
        valid= False
    ret = json.dumps({'msg': msg , 'valid':valid})
    con.close()
    return ret


def is_event_active(id_evento):
    """Comprueba que el evento esté activo
    Args:
        id_evento (string): 
    Returns:
        Boolean
    """
    if (check_evento_exists(id_evento) is False):
        return False
    con = set_connection()
    c = get_cursor(con)
    sql =f"SELECT estado from eventos where id_evento='{id_evento}'"
    c.execute(sql)
    estado = c.fetchone['estado']
    return True if estado ==0 else False



def getNombreEvento(id_evento):
    con = set_connection()
    c = get_cursor(con)
    sql =f"SELECT nombre from eventos where id_evento='{id_evento}'"
    c.execute(sql)
    nombre = c.fetchone()['nombre']
    return  nombre


