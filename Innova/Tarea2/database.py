# -*- coding: utf-8 -*-
import psycopg2

# Clase que contempla el objeto Base de Datos
# Atributos:
#   - name: Nombre de la base de datos a conectarse
#   - user: Usuario para conectarse a la base de datos
#   - conexion: Token de la conexion al servidor
#   - cursor: Cursor para recorrer las tuplas de la base de datos
class database(object):
  name = None
  user = None
  password = None
  conexion = None
  cursor = None  
  
  def __init__(self,name,user,password):
    self.name = str(name)
    self.user = str(user)
    self.password = password
    
  def iniciarConexion(self):
    self.conexion = psycopg2.connect("dbname=%s user=%s password=%s"%(self.name,self.user,self.password))
    self.cursor = self.conexion.cursor(cursor_factory=psycopg2.extras.DictCursor);
    
  def cerrarConexion(self):
    self.cursor.close()
    self.conexion.close()

# Clase que contempla una consulta a la Base de Datos
# Atributos:
#   - descripcion: Una breve reseña de la consulta
#   - cursor: El comando en sql a ejecutar

class consulta(database):
  descripcion = ""
  comando = ""
  
  def __init__(self,des,comm,name,user,password):
    super(consulta,self).__init__(name,user,password)
    self.iniciarConexion();
    self.descripcion = des
    self.comando = comm
    
  def execute(self):
    tuplas = self.cursor.execute(self.comando)    
    return self.cursor.fetchall()

    