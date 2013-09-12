#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
import database

# Variables globales para los datos de la base de datos
dbname = "ingenieria"
dbuser = "gustavo"
dbpass = "12345" 

# Consulta 1
def consulta1():
  
  print("\n-----CONSULTA 1----")
  print("""La lista de productos a que está suscrito cada cliente y el 
plan a que se ha afiliado para ese producto.
-------------------""")

  a = database.consulta("""La lista de productos a que está suscrito cada cliente y el
  plan a que se ha afiliado para ese producto""",
  """select nombrecl,numserie,nombreprod,codplan,nombreplan from 
  (cliente natural join producto) natural join activa natural join plan;""",
  dbname,dbuser,dbpass)
  
  result = a.execute()
  string = str(['Nombre del cliente','Numero de serie del producto,','Nombre del producto',
            'Codigo del Plan','Nombre del plan']) + '\n'
  for i in result:
      string = string + str(i) + '\n'
       
  
  a.comando = """select nombrecl,numserie,nombreprod,codplan,nombreplan from 
  (cliente natural join producto) natural join afilia natural join plan;"""
  
  result = result + a.execute()
  for i in result:
      string = string + str(i) + '\n'
  return(string);



# Consulta 2
def consulta2():
  
  print("\n\n-----CONSULTA 2----")
  print("""La lista de clientes que se encuentran afiliados 
a cada plan.
-------------------""")

  b = database.consulta("""La lista de clientes que se encuentran afiliados 
  a cada plan.""",
  """select codplan,nombreplan,cedula,nombrecl from 
  (cliente natural join producto) natural join activa natural join plan;""",
  dbname,dbuser,dbpass)
  
  result = b.execute()
  
  string = str(['Codigo del Plan','Nombre del plan','Cedula del cliente','Nombre del cliente']) + '\n'
  for i in result:
      string = string + str(i) + '\n'
  
  b.comando = """select codplan,nombreplan,cedula,nombrecl from 
  (cliente natural join producto) natural join afilia natural join plan;"""
  
  result = result + b.execute()
  for i in result:
      string = string + str(i) + '\n'
  
  return(string);
  

  
# Consulta 3
def consulta3():  

  print("\n\n-----CONSULTA 3----")
  print("""Lo que se adeuda a la empresa por concepto de servicios 
consumidos pero no pagados aún por estar amparados por un plan postpago.
-------------------""")

  c = database.consulta("""Lo que se adeuda a la empresa por concepto de servicios 
  consumidos pero no pagados aún por estar amparados por un plan postpago.""",
  """select * from consulta3();""",
  dbname,dbuser,dbpass)
  
  result = c.execute()
  return(str(result));
  

  
# Consulta 4
def consulta4():

  print("\n\n-----CONSULTA 4----")
  print("""Lo adelantado por concepto de prepago que 
corresponde a servicios aún sin consumir.
-------------------""")

  d = database.consulta("""Lo adelantado por concepto de prepago que 
  corresponde a servicios aún sin consumir.""",
  """select * from consulta4()""",
  dbname,dbuser,dbpass)
  
  result = d.execute()
  return(str(result));
  
def main():
    print "Resultado de la consulta 1: \n" + consulta1()
    print "Resultado de la consulta 2: \n" + consulta2()
    print "Resultado de la consulta 3: \n" + consulta3()
    print "Resultado de la consulta 4: \n" + consulta4()
    
if __name__ == '__main__':
    main()
    
    