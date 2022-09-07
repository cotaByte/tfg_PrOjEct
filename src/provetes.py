import auxMethods
import main_client
import main_server

def   main():
    ok = True
    con = main_server.connection()
    c = auxMethods.getCursor(con)
    id = 1660560757324
    nombre= 'Asociacio musical beniopa'
    query = "SELECT * from Banda  where id_banda = '%s' and nombre = %s "
    ok = ok and c.execute(query,(id,nombre))
    ret = c.fetchall()
    
    if (ok):
         print (ret)
    else:
        print ("merda de gos")


main()