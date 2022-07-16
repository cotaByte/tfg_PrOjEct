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
        
        cur= con.cursor()
            
        cur.execute("CREATE TABLE Instrumento(id_Instrumento INTEGER PRIMARY KEY, nombre TEXT)")
        print("TABLE INSTRUMENTO CREATED \n ")
        cur.execute("CREATE TABLE Banda(id_Banda INTEGER PRIMARY KEY, nombre TEXT, poblacion TEXT)") #done
        print("TABLE BANDA CREATED  \n") 
        cur.execute("CREATE TABLE Evento(id_Evento INTEGER PRIMARY KEY, nombre TEXT, poblacion TEXT, data TEXT, estado INTEGER)") #done
        print("TABLE EVENTO CREATED \n")
        cur.execute("CREATE TABLE Miembro(id  INTEGER PRIMARY KEY, nif INTEGER , nombre TEXT, apellido1 TEXT, apellido2 TEXT,id_Instrumento INTEGER, telefono INTEGER, id_Banda INTEGER, director INTEGER, pin INTEGER)")# done
        print("TABLE MIEMBRO CREATED \n")
        cur.execute("CREATE TABLE ListMemeberEvent(id_Evento INTEGER PRIMARY KEY, nif INTEGER, id_Instrumento INTEGER)") #done
        print("TABLE LISTMEMBERVENT CREATED \n")
        cur.execute("CREATE TABLE RequireEvent(id_Require INTEGER PRIMARY KEY,id_Evento INTEGER, id_Instrumento INTEGER, actual INTEGER, max INTEGER)")#
        print("TABLE REQUIEREEVENT CREATED \n")
        con.commit()


    except Exception as ex:
        print(ex)

         
con = postgres_connection()

