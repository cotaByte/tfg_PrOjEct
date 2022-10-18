id = '456876754547'
sql2 = "DELETE FROM miembrobanda WHERE id_miembro ="+str(id)

nombre = 'matraca'
poblacion = 'palmeta'
sqlInsert= "INSERT INTO banda (id_banda, nombre, poblacion) values ('"+id+"','"+nombre+"','"+poblacion+"')" 
print(sqlInsert)