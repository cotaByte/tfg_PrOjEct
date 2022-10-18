from tkinter import E
import psycopg2
from pynvim import Host

def postgres_connection( ) :
    try :
        con = psycopg2.connect(

            host= 'localhost',
            user='postgres',
            password='password',
            database='xarangapp'
        )
        return con
    except Exception as ex:
        print(ex)




def getCursor(conn): 
    cursorObj = conn.cursor()
    return cursorObj


def createDatabase(con):

    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE Instrumento(id_Instrumento INTEGER PRIMARY KEY, nombre TEXT)") #done
    cursorObj.execute("CREATE TABLE Banda(id_Banda INTEGER PRIMARY KEY, nombre TEXT, poblacion TEXT)") #done
    cursorObj.execute("CREATE TABLE Evento(id_Evento INTEGER PRIMARY KEY, nombre TEXT, poblacion TEXT, data TEXT, estado INTEGER)") #done
    cursorObj.execute("CREATE TABLE Miembro(id  INTEGER PRIMARY KEY, nif INTEGER , nombre TEXT, apellido1 TEXT, apellido2 TEXT,id_Instrumento INTEGER, telefono INTEGER, id_Banda, director INTEGER, pin INTEGER)")# done
    cursorObj.execute("CREATE TABLE ListMemeberEvent(id_Evento INTEGER PRIMARY KEY, nif INTEGER, id_Instrumento INTEGER)") #done
    cursorObj.execute("CREATE TABLE RequireEvent(id_Require INTEGER PRIMAR KEY,id_Evento INTEGER, id_Instrumento INTEGER, actual INTEGER, max INTEGER)")#
    con.commit()
con = postgres_connection()
createDatabase(con)
