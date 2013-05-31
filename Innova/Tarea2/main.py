# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
import database

# Método que implementa la primera consulta:
# La lista de productos a que está suscrito cada cliente y el plan a que se
# ha afiliado para ese producto

# Consulta 1
def consulta1():
  
  print("\n-----CONSULTA 1----\n")
  a = database.consulta("""La lista de productos a que está suscrito cada cliente y el
  plan a que se ha afiliado para ese producto""",
  """select nombrecl,numserie,nombreprod,codplan,nombreplan from 
  (cliente natural join producto) natural join activa natural join plan;""",
  "software","becca","12345")
  
  result = a.execute()
  
  a.comando = """select nombrecl,numserie,nombreprod,codplan,nombreplan from 
  (cliente natural join producto) natural join afilia natural join plan;"""
  
  result = result + a.execute()
  return(str(result));

  
  
# Consulta 2
def consulta2():
  print("\n\n-----CONSULTA 2----\n")
  b = database.consulta("""La lista de clientes que se encuentran afiliados 
  a cada plan.""",
  """select codplan,nombreplan,cedula,nombrecl from 
  (cliente natural join producto) natural join activa natural join plan;""",
  "software","becca","12345")
  
  result = b.execute()
  
  b.comando = """select codplan,nombreplan,cedula,nombrecl from 
  (cliente natural join producto) natural join afilia natural join plan;"""
  
  result = result + b.execute()
  return(str(result));
  
  
# Consulta 3
def consulta3():  
  print("\n\n-----CONSULTA 3----\n")
  c = database.consulta("""Lo que se adeuda a la empresa por concepto de servicios 
  consumidos pero no pagados aún por estar amparados por un plan postpago.""",
  """select * from consulta3()""",
  "software","becca","12345")
  
  result = c.execute()
  return(str(result));
  
  
  
# Consulta 4
def consulta4():
  print("\n\n-----CONSULTA 4----\n")
  d = database.consulta("""Lo adelantado por concepto de prepago que 
  corresponde a servicios aún sin consumir.""",
  """select * from consulta4()""",
  "software","becca","12345")
  
  result = d.execute()
  return(str(result));