import Utilidades
import json
import time


def login(dni, pwd):  
    """Funcion para logearse en la aplicación
    Args:
        dni (string) 
        pwd (string)
    Returns:
        JSON
    """
    token = None
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    query = f"SELECT id, dni, pwd,id_instrumento FROM Miembros where dni= '{dni}' and pwd = '{pwd}' limit 1"
    c.execute(query)

    if (c.rowcount == 0):
        msg = 'Credenciales incorrectas'
        ret = json.dumps({'ok': False, 'msg':msg})
        con.close()
        return ret
    else:
        for record in c:
            if (record['dni'] == dni and str(record['pwd']) == pwd):
                token = record['id']
                id_insturmento = record['id_instrumento']
                nombre = Utilidades.get_full_nombre_miembro(token)
                ret = json.dumps(
                    {'token': token, 'nombre': nombre, 'id_instrumento': id_insturmento, 'ok': True})
                con.close()
                return ret


def add_user(dni, nombre, apellido1, apellido2, instrumento, director, tlf, pwd):
    """Añade un miembro a la base de datos
    Args:
        dni (string): 
        nombre (string): 
        apellido1 (string):
        apellido2 (string):
        instrumento (int): 
        director (boolean): 
        tlf (int): 
        pwd(string): 
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    query = 'SELECT dni FROM Miembros'
    c.execute(query)
    for record in c:
        if (record['dni'] == dni):
            data = "El usuario ya existe"
            con.close()
            # Check if the user already exists by using the email
            ret = json.dumps({'msg': data, 'ok': False})
            return ret
    # Get timestamp for the id of the user
    def id(a): return str(round(time.time()*1000)) if a == False else str(round(time.time()*1000))+"D"
    try:
        id_miembro =  id(director)
        sql= f"INSERT INTO Miembros (id,dni, nombre, apellido1, apellido2, id_instrumento, telefono, pwd) VALUES ('{id_miembro}', '{dni}', '{nombre}', '{apellido1}','{apellido2}',{instrumento},{tlf},'{pwd}')"
        print(sql)
        c.execute(sql)
        con.commit()
        data = "Miembro añadido correctamente"
        ok = True
        # Check if the user already exists by using the email
    except:
        data = "Hubo un error añadiendo el nuevo usuario"
        ok = False
    con.close()
    ret = json.dumps({'msg': data, 'ok': ok})
    return ret


def list_miembros(id):
    """Lista todos los miembros de la BD
    Args:
        id (string)
    Returns:
      JSON
    """
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql = f"SELECT m.id,m.dni,m.nombre,m.apellido1,m.apellido2,i.nombre as instrumento, m.telefono FROM Miembros m inner join instrumentos i on i.id_instrumento=m.id_instrumento where m.id <>'{id}'"
    c.execute(sql)
    ret = json.dumps(c.fetchall())
    con.close()
    return ret


def rm_member(id):
    """Elimina  un miembro de la BD
    Args:
        id (String)
    Returns:
        JSON
    """
    con = Utilidades.set_connection()
    sql = f"DELETE FROM Miembros WHERE id ='{id}';"
    sql += f"DELETE FROM miembro_banda WHERE id_miembro ='{id}';"
    try:
        c = Utilidades.get_cursor(con)
        c.execute(sql)
        con.commit()
        con.close()
        data = "El miembro fue eliminado correctamente"
        ret = json.dumps({'msg':data , 'ok':True})
    except:
        data = "Hubo un error al tratar de eliminar el miembro"
        ret = json.dumps({'msg':data , 'ok':False})
    return ret