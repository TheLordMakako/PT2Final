import mysql.connector
from mysql.connector import errorcode

# Obtain connection string information from the portal

config = {
  'host':'proyecto-terminal.mysql.database.azure.com',
  'user':'director@proyecto-terminal',
  'password':'Terla1313',
  'database':'nombrestendencias',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '<path-to-SSL-cert>/DigiCertGlobalRootG2.crt.pem'
}

# Construct connection string

try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Nombre de usuario o password incorrectas")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Base de datos no existe")
  else:
    print(err)
else:
  cursor = conn.cursor()

  # Drop previous table of same name if one exists
  cursor.execute("DROP TABLE IF EXISTS tendencia;")
  print("Borra la tabla (si existe).")

  # Create table
  cursor.execute("CREATE TABLE tendencia (id serial PRIMARY KEY, name VARCHAR(50), tuits INTEGER, grafo INTEGER, fecha TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP);")
  print("Terminando de crear tabla")
  tendencia = "tendencia1"
  contador = 30000
  contador1=20156
  contador2 = 123165
  # Insert some data into table
#   cursor.execute("INSERT INTO tendencia (name, tuits, grafo, fecha) values ('"+tendencia+"',"+str(contador)+", 1 , now());")
#   print("Inserted",cursor.rowcount,"row(s) of data.")
#   cursor.execute("INSERT INTO tendencia (name, tuits, grafo,  fecha) VALUES (%s,%s,%s,%s);", ("TENDENCIA2",contador1, 2, "now()"))
#   print("Inserted",cursor.rowcount,"row(s) of data.")
#   cursor.execute("INSERT INTO tendencia (name, tuits, grafo, fecha) VALUES (%s,%s,%s,%s);", ("TENDENCIA3", +contador2, 3,"now()"))
#   print("Inserted",cursor.rowcount,"row(s) of data.")

  # Cleanup
  conn.commit()
  cursor.close()
  conn.close()
  print("Done.")