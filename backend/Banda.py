import Utilidades
import json
import time


def add_banda(nombre, poblacion):
    """Añade una banda a la BD
    Args:
        nombre (string)
        poblacion (string)
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    query = 'SELECT nombre FROM Bandas'
    c.execute(query)
    for record in c:
        if (record['nombre'] == nombre):
            data = "Esta banda ya se encuentra registrada"
            # Check if the user already exists by using the email
            ret = json.dumps({'msg': data, 'ok': False})
            con.close()
            return ret
    id = str(round(time.time()*1000))
    sql = f"INSERT INTO Banda (id_banda, nombre, poblacion) VALUES ('{id}', '{nombre}', '{poblacion}')"
    try:          
        c.execute(sql)
        con.commit()
        con.close()
        data = "Banda añadida correctamente"
        ok=True
    except:
        data = "Eror al añadir la banda"
        ok=False
    # Check if the user already exists by using the email
    ret = json.dumps({'msg': data, 'ok':ok})
    return ret


def list_bandas():
    """Devuelve el listado de las  bandas que existen
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    c.execute("SELECT * FROM Bandas order by id_banda desc")
    data = c.fetchall()
    c.close()
    return json.dumps(data) 


def join(token,  id_banda):
    """Une un miembro y una banda
    Args:
        token (String)
        id_banda (String)
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql = f"SELECT nombre FROM Bandas WHERE id_banda = '{id_banda}' "
    c.execute(sql)
    record_set = c.fetchone()
    nombre_banda = record_set['nombre']
    c.execute (f"SELECT id_miembro, id_banda FROM miembro_banda WHERE id_miembro = '{token}' AND id_banda = '{id_banda}'")
    c.fetchall()
    if (c.rowcount!=0):
        con.close()
        data = "El miembro ya se encuentra en esta banda"
        ret = json.dumps({'msg': data, 'ok':False})
        return ret
    try:
        sql_insert = f"INSERT INTO miembro_banda (id_miembro,id_banda) VALUES ('{token}', '{id_banda}' )"
        c.execute(sql_insert)
        con.commit()
        data = "Te has añadido a la banda  "+nombre_banda+" correctamente"
        con.close()
        ret = json.dumps({'msg': data, 'ok': True})
    except:
        con.close()
        data = "Hubo un error al intentar unirse a esta banda"
        ret = json.dumps({'msg': data, 'ok': False})
    return ret 


def list_join(token):
    """Lista las bandas disponibles para unirse
    Args:
        token (String)
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql = f" select * from Bandas where id_banda not in (select id_banda from miembro_banda where id_miembro= '{token}' );"
    c.execute(sql)
    data = c.fetchall()
    ret = json.dumps(data)
    c.close()
    return ret


def list_leave(token):
    """Lista las bandas disponibles para abandonar
    Args:
        token (String)
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql = f" select * from Bandas where id_banda in (select id_banda from miembro_banda where id_miembro= '{token}' );"
    c.execute(sql)
    data= c.fetchall()
    c.close()
    ret = json.dumps(data)
    return ret


def leave(token, id_banda):
    """Elimina a un miembro que estaba unido a una banda
    Args:
        token (String)
        id_banda (String)
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql = f"SELECT nombre FROM Bandas WHERE id_banda = '{id_banda}' " 
    c.execute(sql)
    record_set = c.fetchone()
    nombre_banda = record_set['nombre']
    query = f"DELETE FROM miembro_banda WHERE id_miembro = '{token}' AND id_banda = '{id_banda}'"
    try:
        Utilidades.get_cursor(con).execute(query)
        con.commit()
        con.close()
        data = "Has abandonado la banda" + nombre_banda
        ret = json.dumps({'msg': data, 'ok': True})
    except:
        con.close()
        data = "No se ha podido abandonar la banda"
        ret = json.dumps({'msg': data, 'ok': False})
    return ret


def rm_banda(id):
    """Elimina una banda de la  BD
    Args:
        id (string): id de la banda
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    sql = f"DELETE FROM Bandas WHERE id_banda ='{id}';"
    sql += f"DELETE FROM miembro_banda WHERE id_banda ='{id}';"
    try:
        c = Utilidades.get_cursor(con)
        c.execute(sql)
        con.commit()
        con.close()
        data = "La banda fue eliminada correctamente"
        ret = json.dumps({'msg':data , 'ok':True})
        return ret
    except:
        data = "Hubo un error al tratar de eliminar la banda"
        ret = json.dumps({'msg':data , 'ok':False})
        return ret