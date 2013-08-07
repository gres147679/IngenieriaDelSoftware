#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# Para este módulo se han implementado dos clases:
# -La clase consumo: Describe un consumo que será agregado a la base de datos
#
# -La clase consulta: Describe un pedido de lista de consumos que se hará en la
#  base de datos. Considerando los requerimientos de Innova, se piden consumos
#  para un mes de facturación en particular

import psycopg2
import database
import consumos
import dbparams

class consumo:
  """
  Define un consumo a agregar en la base de datos.
  """
  
  def __init__(self,numserie,fecha,codservicio,cantidad):
    """
    Construye un nuevo consumo, y lo agrega a la base de datos.
    Debe existir un plan o paquete que incluya el servicio que se 
    consume
    
    Parametros:
      -El número de serie del producto que consume
      -La fecha del consumo. En formato de string DD/MM/AAAA
      -El código del servicio que se consume
      -La cantidad de unidades consumidas
    """
    
    self.numserie = numserie
    self.fecha = fecha
    self.codservicio = codservicio
    self.cantidad = cantidad
    
    # Conexión con la base de datos
    self.conexiondb = database.operacion(
      'Operacion que inserta un consumo en la DB',
      'insert into consume values (\'%s\',%s,\'%s\',%s);' 
      % (self.numserie,self.fecha,self.codservicio,self.cantidad),
      dbparams.dbname,dbparams.dbuser,dbparams.dbpass
      )
    
    self.conexiondb.execute()
    
    import consumos;consumos.consumo("CBZ27326",1001,"31/05/2013",50)