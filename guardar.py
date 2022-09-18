import mysql.connector

conexion1=mysql.connector.connect(host="db4free.net", 
                                  user="dbpruebas78", 
                                  passwd="E=mc2a+b0929", 
                                  database="dbpruebas78")
cursor1=conexion1.cursor()
sql="INSERT INTO estacion(id, n_carro) values ('%s','%s')"
datos = (0,1)
res = cursor1.execute(sql, datos)   
print(res)