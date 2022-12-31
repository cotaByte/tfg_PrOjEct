import Utilidades
import json
import time


def login(nif, pin):  # Method to log in on  website
    token = None
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    query = f'SELECT id, nif, pin,id_instrumento FROM Miembros where nif= {nif} and pin= {pin} limit 1'
    c.execute(query)

    if (c.rowcount == 0):
        ret = json.dumps({'ok': False})
        con.close()
        return ret
    else:
        for record in c:
            if (record['nif'] == int(nif) and str(record['pin']) == str(pin)):
                token = record['id']
                id_insturmento = record['id_instrumento']
                nombre = Utilidades.get_full_nombre_miembro(token)
                ret = json.dumps(
                    {'token': token, 'nombre': nombre, 'id_instrumento': id_insturmento, 'ok': True})
                con.close()
                return ret


def add_user(nif, nombre, apellido1, apellido2, instrumento, director, tlf, pin):
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    query = 'SELECT nif FROM Miembros'
    c.execute(query)
    for record in c:
        if (record['nif'] == nif):
            data = "El usuario ya existe"
            con.close()
            # Check if the user already exists by using the email
            ret = json.dumps({'msg': data, 'ok': False})
            return ret

    # Get timestamp for the id of the user
    def id(a): return str(round(time.time()*1000)
                          ) if a == False else str(round(time.time()*1000))+"D"
    print(id(director) + "\n")
    try:
        c.execute('INSERT INTO Miembros (id, nif, nombre, apellido1, apellido2, id_instrumento, telefono, pin) VALUES (%s, %s, %s, %s, %s, %s,%s,%s)', (id(
            director), nif, nombre, apellido1, apellido2, instrumento, tlf, pin))
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
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql = f"SELECT id,nif,nombre,apellido1,apellido2,id_instrumento, telefono FROM Miembros where id <>'{id}'"
    c.execute(sql)
    ret = json.dumps(c.fetchall())
    con.close()
    return ret


def rm_member(id):
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
        ret = json.dumps({'msg':data , 'ok':True})
    return ret