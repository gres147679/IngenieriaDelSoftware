#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
import database

# Método que implementa la primera consulta:
# La lista de productos a que está suscrito cada cliente y el plan a que se
# ha afiliado para ese producto

def main():
  
  # Consulta 1
  print("\n-----CONSULTA 1----")
  print("""La lista de productos a que está suscrito cada cliente y el 
plan a que se ha afiliado para ese producto.
-------------------""")
  a = database.consulta("""La lista de productos a que está suscrito cada cliente y el
  plan a que se ha afiliado para ese producto""",
  """select nombrecl,numserie,nombreprod,codplan,nombreplan from 
  (cliente natural join producto) natural join activa natural join plan;""",
  "software","becca","12345")
  
  result = a.execute()
  
  a.comando = """select nombrecl,numserie,nombreprod,codplan,nombreplan from 
  (cliente natural join producto) natural join afilia natural join plan;"""
  
  result = result + a.execute()
  print(str(result));

  
  
  # Consulta 2
  print("\n\n-----CONSULTA 2----")
  print("""La lista de clientes que se encuentran afiliados 
a cada plan.
-------------------""")
  b = database.consulta("""La lista de clientes que se encuentran afiliados 
  a cada plan.""",
  """select codplan,nombreplan,cedula,nombrecl from 
  (cliente natural join producto) natural join activa natural join plan;""",
  "software","becca","12345")
  
  result = b.execute()
  
  b.comando = """select codplan,nombreplan,cedula,nombrecl from 
  (cliente natural join producto) natural join afilia natural join plan;"""
  
  result = result + b.execute()
  print(str(result));
  
  
  
  # Consulta 3
  print("\n\n-----CONSULTA 3----")
  print("""Lo que se adeuda a la empresa por concepto de servicios 
consumidos pero no pagados aún por estar amparados por un plan postpago.
-------------------""")
  c = database.consulta("""Lo que se adeuda a la empresa por concepto de servicios 
  consumidos pero no pagados aún por estar amparados por un plan postpago.""",
  """select * from consulta3()""",
  "software","becca","12345")
  
  result = c.execute()
  print(str(result));
  
  
  
  # Consulta 4
  print("\n\n-----CONSULTA 4----")
  print("""Lo adelantado por concepto de prepago que 
corresponde a servicios aún sin consumir.
-------------------""")
  d = database.consulta("""Lo adelantado por concepto de prepago que 
  corresponde a servicios aún sin consumir.""",
  """select * from consulta4()""",
  "software","becca","12345")
  
  result = d.execute()
  print(str(result));
  
  
  
if __name__ == '__main__':
  main()