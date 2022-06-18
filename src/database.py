import sqlite3
from sqlite3 import Error

# Creación de la conexión con la base de datos
def sql_connection():
    try:
        con = sqlite3.connect('databse.db')
        return con
    except Error:
        print(Error)




def sql_table(con):

    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE Instrumento(id_Instrumento INTEGER PRIMARY KEY, nombre TEXT)") #done
    cursorObj.execute("CREATE TABLE Banda(id_Banda INTEGER PRIMARY KEY, nombre TEXT, poblacion TEXT)") #done
    cursorObj.execute("CREATE TABLE Evento(id_Evento INTEGER PRIMARY KEY, nombre TEXT, poblacion TEXT, data TEXT, estado INTEGER)") #done
    cursorObj.execute("CREATE TABLE Miembro(nif INTEGER PRIMARY KEY, nombre TEXT, apellido1 TEXT, apellido2 TEXT,id_Instrumento INTEGER, telefono INTEGER, id_Banda, director INTEGER, pin INTEGER)")# done
    cursorObj.execute("CREATE TABLE ListMemeberEvent(id_Evento INTEGER PRIMARY KEY, nif INTEGER, id_Instrumento INTEGER)") #done
    cursorObj.execute("CREATE TABLE RequireEvent(id_Require INTEGER PRIMAR KEY,id_Evento INTEGER, id_Instrumento INTEGER, actual INTEGER, max INTEGER)")#
    con.commit()
con = sql_connection()
sql_table(con)


'''
Aclaraciones:

- El login se realizará comporbando el nif y el correspondiente pin del miembro
- En la tabla miembro, el campo director se instanciará a 0 o 1 para otorgar privilegios de creación de eventos (0 -> not director, 1 -> director)
- En la tabla evento el campo estado indicará si es posible la inscripción en el evento (0 -> not avalible , 1 -> avalible )
- Este archivos solamente debe de ejecutarse en el momento de instanciación de la base de datos.INTEGER
- Los instrumentos de la tabla se cargarán previamente, ya que para la ejecución de la app no se contempla añadir instrumentos (ya existen todos los instrumentos)

'''