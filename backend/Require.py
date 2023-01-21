import Utilidades
import json
import time
    
def insert_requirement(id_evento, instrumento, num_max):

    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql = "select * from requerimientos_evento where id_evento  ='" + \
        str(id_evento)+"' and id_instrumento   ='"+str(instrumento)+"'"
    c.execute(sql)
    if (c.rowcount != 0):
        con.close()
        data = "Ya existe un require registrado con este codigo"
        ret = json.dumps({'msg': data, 'ok': False})
        return ret
    id = str(round(time.time()*1000))
    sql_insert = "INSERT INTO requerimientos_evento (id_require, id_evento,id_instrumento,max) values (%s,%s,%s,%s)"
    c.execute(sql_insert, (id, id_evento, instrumento, num_max))
    con.commit()
    con.close()
    data = "El require se ha insertado  correctamente"
    ret = json.dumps({'msg': data, 'ok': True})
    return ret




def list_requirements_for_event(id_miembro,id_evento):
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql = f"select req.*, ins.nombre  as nombre_instrumento from requerimientos_evento req inner join instrumentos ins on ins.id_instrumento = req.id_instrumento where req.id_evento  ='{id_evento}'"
    inscrito = Utilidades.esta_miembro_inscrito_en_evento(id_miembro,id_evento)
    c.execute(sql)
    data = c.fetchall()
    c.close()
    ret = json.dumps({'data': data, 'inscrito': inscrito})
    return ret

def remove_requerimiento(id_req):
    con = Utilidades.set_connection()
    c = Utilidades.get_cursor(con)
    sql =f"delete from requerimientos_evento where id_require= '{id_req}'"
    try:
        c.execute(sql)
        sql =f"delete from eventos_miembros_inscritos where id_require ='{id_req}'"
        c.execute()
        con.commit()
        msg= 'El requerimiento se fue eliminado correctamente'
        ok= True
    except:
        msg= 'El requerimiento no pudo borrarse correctamente'
        ok= False
    ret = json.dumps({'msg': msg , 'ok':ok})
    con.close()
    return ret
