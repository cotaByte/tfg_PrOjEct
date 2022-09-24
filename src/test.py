import json
import auxMethods
import main_server
from psycopg2.extras import RealDictCursor
def con2():
    con = main_server.connection()
    c = auxMethods.getCursor(con)
    c.execute("select * from miembro")
    a=c.fetchall()
    r= json.dumps(a)
    print (r)
    
    
con2()
    
    