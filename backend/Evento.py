import Utilidades
import json
import time


def register_event(nombre, ubicacion, fecha_evento, estado):
    """Añade un evento a la BD
    Args:
        nombre (String): _description_
        ubicacion (String): _description_
        fecha_evento (Date): _description_
        estado (Int): 1 si esta cerrado | 0 si esta operativo
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql = f"SELECT nombre FROM eventos WHERE nombre = '{nombre}'" 
    c.execute(sql)
    if (c.rowcount != 0):
        con.close()
        data = "Ya existe un evento registrado con este codigo"
        # Check if the event is already registered
        ret = json.dumps({'msg': data, 'ok': False})
        return ret
    id = str(round(time.time()*1000))
    try:
        c.execute('INSERT INTO eventos (id_evento, nombre, ubicacion,fecha_evento,estado) VALUES (%s, %s, %s,%s,%s) ',(id, nombre, ubicacion, fecha_evento, estado))
        con.commit()
        data = "Evento añadido correctamente"
        ok = True
    except:
        data = "Hubo un error al añadir el evento"
        ok = False
    con.close()
    ret = json.dumps({'msg': data, 'ok': ok})
    return ret

def list_events():
    """Lista todos los eventos activos
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    c.execute("SELECT * FROM Eventos WHERE estado <> 1")
    data= c.fetchall()
    c.close()
    ret = json.dumps(data)
    return ret


def rm_evento(id):
    """Elimina un evento de la BD (Ojo!! Controlamos el borrado en cascada)
    Args:
        id (String):  id del evento a borrar
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    try:
        sql = f"DELETE FROM Eventos WHERE id_evento ='{id}';"
        sql+= f"DELETE FROM eventos_miembro_inscritos where id_evento ='{id}';"
        sql+= f"DELETE FROM requerimientos_evento where id_evento ='{id}';"
        c = Utilidades.get_cursor(con)
        c.execute(sql)
        con.commit()
        con.close()
        data = "El evento fue eliminado correctamente"
        ret = json.dumps({'msg': data, 'ok': True})
        return ret
    except:
        data = "Hubo un error al tratar de eliminar el evento"
        ret = json.dumps({'msg': data, 'ok': False})
        return ret


def inscribe_to_an_event( id_miembro, id_require,id_evento): 
    """Insribirse en un evento
    Args:
        id_miembro (String)
        id_require (String)
        id_evento (String)
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    ret = ""
    data = "Has sido inscrito en el evento correctamente"
    if (Utilidades.check_evento_exists(Utilidades.get_evento_require(id_require)) is False):
        data = "El evento no existe"
        ret = json.dumps({'msg': data, 'ok': False})
        con.close()
        return ret
    sql =f"SELECT * FROM eventos_miembro_inscritos where id_miembro = '{id_miembro}' and id_require = '{id_require}'"
    c.execute(sql)
    if (c.rowcount != 0): #si ya esta el miembro inscrito o no
        con.close()
        data = "Ya estas inscrito en este evento"
        ret = json.dumps({'msg': data, 'ok': False})
        con.close()
        return ret
    sql = f"SELECT * from requerimientos_evento where id_require = '{id_require}' and id_evento = '{id_evento}' and actual=max"
    print(sql)
    c.execute(sql)
    if (c.rowcount!=0): #si el requerimiento ya esta a full o no
        data = "El requerimiento para este evento respecto a este instrumento está ya completo"
        ret = json.dumps({'msg': data, 'ok': False})
        con.close()
        return ret
    sql = f"select id_instrumento from requerimientos_evento where id_require = '{id_require}'"    
    c.execute(sql)
    res=c.fetchone()
    inst_require = res['id_instrumento']
    inst_miembro  = Utilidades.get_miembro_instrumento(id_miembro)
    if (inst_require!=inst_miembro):
        con.close()
        data = "El usuario no tiene asignado este instrumento"
        ret = json.dumps({'msg': data, 'ok': False})
        con.close()
        return ret
    sql = f"SELECT * FROM eventos_miembro_inscritos where id_miembro = '{id_miembro}' and id_require = '{id_require}'"
    c.execute(sql)
    if (c.rowcount != 0):
        con.close()
        data = "Ya estas inscrito en este evento"
        ret = json.dumps({'msg': data, 'ok': False})
        return ret
    sql_insert = "INSERT INTO  eventos_miembro_inscritos (id_evento, id_miembro, id_require) VALUES    (%s,%s,%s)"
    c.execute(sql_insert, (id_evento, id_miembro,id_require))
    sql_update = f"UPDATE requerimientos_evento SET actual  = actual+1 where id_require = '{id_require}' "
    c.execute(sql_update)
    con.commit()
    con.close()
    ret = json.dumps({'msg': data, 'ok': True})
    return ret


def close_event(id_evento):
    """Cerrar el evento
    Args:
        id_evento (String)
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql= f"update eventos set estado = 1 where id_evento = '{id_evento}' "
    try:
        c.execute(sql)
        con.commit()
        data = "El evento se ha cerrado  correctamente"
        ret = json.dumps({'msg': data, 'ok': True})
    except:
        data = "No se ha podido cerrar el evento"
        ret = json.dumps({'msg': data, 'ok': False})
    con.close()    
    return ret


def desinscribe_for_event(id_req,token):
    """Desinscribe un miembro de un require
    Args:
        id_req (String)
        token (Stirng)
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql =f"delete from eventos_miembro_inscritos where id_require= '{id_req}' and id_miembro ='{token}';"
    sql += f"update requerimientos_evento set actual=actual-1 where id_require ='{id_req}';"
    try:
        c.execute(sql)
        msg= 'Te has desinscrito del evento'
        ok= True
    except:
        msg= 'Hubo un error al tratar de desinscribirse del evento'
        ok= False
    ret = json.dumps({'msg': msg , 'ok':ok})
    con.commit()
    con.close()
    return ret