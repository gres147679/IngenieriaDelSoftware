# Clase moduloCliente.py
#!/usr/bin/env python
#!/usr/bin/py
# -*- coding: utf-8 -*-

import sys
import cliente

#Librerias de conexion con postgresql
import psycopg2
import psycopg2.extras

class moduloCliente:
    
    #
    # Se inicializa la clase moduloCliente
    #
    def __init__(self):
        self.db = 'tarea03';
        try:
            #Se conecta a la base de datos
            self.conexion = psycopg2.connect(database=self.db, user="postgres", password="123456")
        except:
            print "No se pudo conectar a la base de datos."
            sys.exit()      
            
    #
    # Se cierra la conexion con la base de datos.
    #    
    def cerrarConexion(self):
        self.conexion.close()

    #
    # Se verifica si la tabla CLIENTE esta vacia
    #
    def tablaVacia(self):
        cursorCliente = self.conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Se calcula cuantos elementos fueron encontrados
        contador = self.conexion.cursor()
        contador.execute("SELECT COUNT(*) FROM CLIENTE")
        result=contador.fetchone()
        number_of_rows = result[0]
        
        contador.close()
        self.conexion.commit()
        cursorCliente.close()
        
        return (number_of_rows == 0)

    #
    # Indica si un cliente se encuentra o no en la base de datos.
    #     
    def existeCliente(self, idCliente):
        cursorCliente = self.conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Se calcula cuantos elementos fueron encontrados
        contador = self.conexion.cursor()
        contador.execute("SELECT COUNT(*) FROM CLIENTE WHERE cedula = %(cedula)s",{'cedula' : idCliente})
        result=contador.fetchone()
        number_of_rows = result[0]
        
        contador.close()
        self.conexion.commit()
        cursorCliente.close()
        
        #Indica si se encuentra el cliente o no. 
        return (number_of_rows > 0)
      
    #
    # Obtiene y valida el id de un cliente por consola.
    #
    def validarId(self):
        while True:
            # Verifica que la entrada sea un entero.
            try:
                x = int(raw_input('Introduzca la cedula del cliente: '))
            except ValueError:
                print "ERROR: Debe ser un numero.\n"
            else:
                #Verifica que sea un entero positivo.
                if (x <= 0):
                    print "ERROR: Debe ser un numero.\n"
                else:
                    return str(x)

    #
    # Obtiene y valida los datos de un cliente insertados por consola
    #
    def datosCliente(self):
        print("Introduzca los siguientes datos: ")
                
        # Verifica que la entrada de la cedula sea valida
        while True:
            # Verifica que la entrada sea un entero.
            try:
                x = int(raw_input('    Cedula: '))
            except ValueError:
                print "    ERROR: Debe ingresar un numero."
            else:
                #Verifica que sea un entero positivo.
                if (x <= 0):
                    print "    ERROR: Debe ingresar un numero positivo."         
            if (self.existeCliente(x)):
                print "\nERROR: La cedula introducida ya se encuentra en el sistema. Intente de nuevo.\n"
            else:   
                ci = str(x)
                break
        
        # Verifica que la entrada del nombre sea valida.
        while True:
            nombre = raw_input('    Nombre: ')

            #Verifica que sea distinto de una cadena vacia
            if (nombre == ""):
                print "    ERROR: Entrada no valida."
                continue
            break 
        
        # Verifica que la entrada de la direccion sea valida.
        while True:
            direccion = raw_input('    Direccion: ')

            #Verifica que sea distinto de una cadena vacia
            if (direccion == ""):
                print "    ERROR: Entrada no valida."
                continue
            break 
          
        return (ci,nombre,direccion)

    #
    # Se registra un cliente.
    #
    def registroCliente(self):
        cursorRegistro = self.conexion.cursor(cursor_factory = psycopg2.extras.DictCursor)
                
        #Inserta el cliente introducido
        datos = self.datosCliente()
       
        cursorRegistro.execute("INSERT INTO CLIENTE (cedula,nombrecl,direccion) VALUES (%s,%s,%s);",datos)
        print "\nEl cliente se ha registrado exitosamente."     
     
        self.conexion.commit()
        cursorRegistro.close()

    #
    # Se consulta un cliente
    #     
    def consultaClientes(self):
        cursorCliente = self.conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        flag = True
        
        #Se verifica que la base de datos no este vacia
        if self.tablaVacia():
            print "ERROR: No se puede consultar al cliente. La base de datos esta vacia.\n"
        else:
            idCliente = self.validarId()
            #Se verifica que la cedula introducida exista
            while flag:    
                if (self.existeCliente(idCliente)):
                    cursorCliente.execute("""SELECT cedula, nombrecl, direccion FROM CLIENTE 
                                          WHERE cedula = %(cedula)s""",{'cedula' : idCliente})                    
                    for row in cursorCliente.fetchall():
                        writeRow = 'Cedula: ' + str(row['cedula'])
                        writeRow += ' Nombre: ' + row['nombrecl']
                        writeRow += ' Direccion: ' + str(row['direccion'])               
                        print writeRow
                    flag = False
                else:
                    print "\nERROR: La cedula introducida no se encuentra en el sistema. Intente de nuevo.\n"
                    idCliente = raw_input('Introduzca la cedula del cliente: ')
      
        self.conexion.commit()
        cursorCliente.close()
     
    #
    # Se busca un cliente, y retorna sus datos en la clase Cliente.
    # Si el cliente no se encuentra en la base de datos, retorna None.
    #     
    def busquedaCliente(self, idCliente):
        cursorCliente = self.conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        #Se verifica que la base de datos no este vacia
        cliente = None
        if self.tablaVacia():
            print "\nERROR: No se puede buscar al cliente. La base de datos esta vacia."
        else:        
            if (self.existeCliente(idCliente)):
                cursorCliente.execute("""SELECT cedula, nombrecl, direccion FROM CLIENTE 
                                      WHERE cedula = %(cedula)s""",{'cedula' : idCliente})                
                for row in cursorCliente.fetchall():
                    writeRow = 'Cedula: ' + str(row['cedula'])
                    writeRow += ' Nombre: ' + row['nombrecl']
                    writeRow += ' Direccion: ' + str(row['direccion'])
                    
                    cliente = cliente.cliente(row['cedula'], row['nombrecl'], row['direccion'])
                        
        self.conexion.commit()
        cursorCliente.close()
        
        return cliente

          
#MAIN DE PRUEBA        
# if __name__== "__main__":
#        
#     moduloCl = moduloCliente()
#     moduloCl.registroCliente()
#        
#     moduloCl.consultaClientes() 
#         
#     cl = moduloCl.busquedaCliente(1243)
#     if cl!= None:
#         print str(cl)
#     else:
#         print "No existe"   
#    
#     if moduloCl.existeCliente(123):
#         print "found"
#     else:
#         print "not found"
#     moduloCl.cerrarConexion()
    
    
#END moduloCliente.py