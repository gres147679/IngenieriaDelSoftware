# -*- coding: utf-8 -*-
import psycopg2
import database

# Método que implementa la primera consulta:
# La lista de productos a que está suscrito cada cliente y el plan a que se
# ha afiliado para ese producto

def main():
  # Consulta 1
  b = database.consulta("""La lista de productos a que está suscrito cada cliente y el
  plan a que se ha afiliado para ese producto""",
  """select nombrecl,numserie,codplan from 
  (cliente natural join producto) natural join activa;""",
  "ingsoftware","gustavo")
  
  result = b.execute()
  
  b.comando = """select nombrecl,numserie,codplan from 
  (cliente natural join producto) natural join afilia;"""
  
  result = result + b.execute()
  print str(result)
  
  
  
if __name__ == '__main__':
  main()