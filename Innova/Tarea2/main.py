# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
import database

# Método que implementa la primera consulta:
# La lista de productos a que está suscrito cada cliente y el plan a que se
# ha afiliado para ese producto

def main():
  # Consulta 1
  a = database.consulta("""La lista de productos a que está suscrito cada cliente y el
  plan a que se ha afiliado para ese producto""",
  """select nombrecl,numserie,codplan from 
  (cliente natural join producto) natural join activa;""",
  "ingenieria","gustavo","gustavo1994")
  
  result = a.execute()
  
  a.comando = """select nombrecl,numserie,codplan from 
  (cliente natural join producto) natural join afilia;"""
  
  result = result + a.execute()
  print(str(result));
  
  # Consulta 3
  
  c = database.consulta("""Lo que se adeuda a la empresa por concepto de servicios 
  consumidos pero no pagados aún por estar amparados por un plan postpago.""",
  """select * from consulta3()""",
  "ingenieria","gustavo","gustavo1994")
  
  result = c.execute()
  print(str(result));
  
  
if __name__ == '__main__':
  main()