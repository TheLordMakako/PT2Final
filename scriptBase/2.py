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
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()
  contador1= 22881
  tendencia = "Jagger"
  grafo = 9
  # Read data
  
  
  #cursor.execute("UPDATE tendencia SET tuits = %s WHERE name = %s;", (contador1, tendencia))
  cursor.execute("SELECT * FROM tendencia where name = '"+tendencia+"';")
  rows = cursor.fetchall()
  if (cursor.rowcount > 0):
    cursor.execute("UPDATE tendencia SET tuits = %s, grafo = %s WHERE name = %s;", (contador1, grafo, tendencia))
    print("ya hay uno igual, actualizamos")
  else:
      cursor.execute("INSERT INTO tendencia (name, tuits, grafo, fecha) values ('" + tendencia + "',"+str(contador1)+","+str(grafo) +",now());")
      print("No hay uno igual, se inserta")

  cursor.execute("SELECT * FROM tendencia order by tuits desc limit 10;")
  rows = cursor.fetchall()
  #Print all rows
  for row in rows:
  	print("Data row = (%s, %s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]),str(row[3]), str(row[4]) ))

  # Cleanup
  conn.commit()
  cursor.close()
  conn.close()
  print("Done.")