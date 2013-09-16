##***************************************************************************
##************************MODULO DE AFILIACIONES ****************************
##***************************************************************************

##*** Librerias a utilizar **************************************************

import psycopg2
import psycopg2.extras
import unittest
import database
import dbparams
##*** Clase de Afiliaciones *************************************************

class Afiliaciones:
    nombreBase = dbparams.dbname
    usuarioBase = dbparams.dbuser
    passwordBase = dbparams.dbpass
    ## Constructor de la clase
    def __init__ (self,serie_producto,cod_plan):
        self.producto = serie_producto
        self.plan = cod_plan

##*** Metodos de la clase ***************************************************
    
    ## Devuelve algun producto
    def getProducto (self):
        return self.producto
        
    ## Devuelve algun codigo de plan
    def getPlan (self):
        return self.plan
        
    ## Guarda los cambios realizados en la base de datos
    def guardarCambios(self):
        self.conectar.commit()
        
    ## Pide al usuario que determine el tipo de plan al que desea afiliar su 
    ## producto
    def tipoPlan (self):
        tipoplan = 0
        while (tipoplan != '1' and tipoplan != '2'):
            tipoplan = raw_input("""Indique si el plan es 'infinito' o 'paquete'
            Ingrese 1 si es infinito
            Ingrese 2 si es un paquete
            """)
            
        if tipoplan == '1':
            plan = 'infinito'
        else:
            plan = 'paquete' 
            
        return plan
                    
    ## 
    ## Verifica si un plan esta presente en la base de datos. Si existe lo devuelve,
    ## si no, muestra un mensaje de error
    def buscarPlan(self):
        try:
            conexion = database.operacion("","""SELECT tipo FROM PLAN WHERE
            codplan= %s"""%(self.plan),Afiliaciones.nombreBase,Afiliaciones.usuarioBase,
            Afiliaciones.passwordBase)
            resultado = conexion.execute()
            conexion.cerrarConexion()
            
            ## Si el plan no se consigue
            if len(resultado) == 0:
                raise Exception("El plan introducido no existe en la base de datos.")
            
            ## Si se consigue el plan, se devuelve 
            return resultado[0][0]
            
        except Exception, e:
            print "\nERROR: ", e
    
    # Crea la afiliacion de un producto con un plan
    def CrearAfiliacion (self):
        try:            
            tipoplan = self.buscarPlan()
            
            # Si el plan no existe
            if tipoplan != 'infinito' and tipoplan != 'paquete':
                raise Exception("No se pudo realizar la afiliacion. Favor verifique su plan")

            # Buscamos el producto que desea afiliarse en la base de datos
            conexion = database.operacion("","""SELECT * FROM PRODUCTO WHERE 
                    numserie= '%s'"""%(self.producto),Afiliaciones.nombreBase,
                    Afiliaciones.usuarioBase,Afiliaciones.passwordBase)
            resultado = conexion.execute()
            
            ## Si el producto no existe en la base de datos.
            if len(resultado) == 0:
                raise Exception("El producto introducido no existe en la base de datos")
            
            
            ## Verificamos si el producto ya esta afiliado a un plan prepago
            conexion.setComando("""SELECT * FROM ACTIVA WHERE 
                                numserie = '%s'"""%(self.producto))
            resultado = conexion.execute()
            
            ## Si el producto ya tiene plan
            if len(resultado) != 0:
                raise Exception("El producto introducido ya tiene un plan asociado")
            
            ## Verificamos si el producto ya esta afiliado a un plan postpago
            conexion.setComando("""SELECT * FROM AFILIA WHERE 
                                numserie = '%s'"""%(self.producto)), 
            resultado = conexion.execute()
            
            ## Si el producto ya tiene plan
            if len(resultado) != 0:
                raise Exception("El producto introducido ya tiene un plan asociado")
     

            ## Si el plan es prepago
            print tipoplan
            if tipoplan == 'prepago':
                conexion.setComando("""INSERT INTO ACTIVA VALUES 
                ('%s', %s, %s)"""%(self.producto, self.plan, 0))
                
                
            ## Si el plan es postpago
            else:
                plan = self.tipoPlan()
                conexion.setComando("""INSERT INTO AFILIA VALUES 
                ('%s', %s, '%s')"""%(self.producto, self.plan, plan))
                
            resultado = conexion.execute()
            print """\nSe ha afiliado el producto %s con el plan %s exitosamente
            """%(self.producto,self.plan)
            
            ## Guardamos los cambios y cerramos la conexion
            conexion.conexion.commit()
            conexion.cerrarConexion()
            
        ## Capturamos los posibles errores.
        except Exception, e:
            print '\nERROR: ', e
            
    ## Crea una afiliacion entre un producto y un paquete de servicios
    def CrearContratacion (self):
        try:
            
            ## Verificamos si el paquete existe en la base de datos
            conexion = database.operacion("","""SELECT codpaq FROM PAQUETE 
                WHERE codpaq = %s"""%(self.plan),Afiliaciones.nombreBase,
                Afiliaciones.usuarioBase,Afiliaciones.passwordBase)
            resultado = conexion.execute()
            
            
            if len(resultado) == 0:
                raise Exception("El paquete introducido no existe en la base de datos")
            
            # Verificamos si la contratacion ya existe en la base de datos
            conexion.setComando("""SELECT codpaq, numserie FROM CONTRATA 
            WHERE codpaq = %s AND numserie = '%s'"""%(self.plan,self.producto))
       
            resultado = conexion.execute()
            if len(resultado) != 0:
                raise Exception("La afiliacion entre dichos producto y paquete ya existe")
            
            # Si la contratacion no existia, la creamos
            conexion.setComando("""INSERT INTO CONTRATA VALUES 
            ('%s', %s)"""%(self.producto, self.plan))
            
            resultado = conexion.execute()
            print ("""\nSe ha creado la afiliacion del producto de codigo %s \
con el paquete de codigo %s""")%(self.producto, self.plan)
            
            ## Guardamos los cambios y cerramos la base de datos
            conexion.conexion.commit()
            conexion.cerrarConexion()
            
        ## Capturamos los posibles errores.
        except Exception, e:
            print '\nERROR: ', e
            
    ## Elimina la afiliacion entre un producto y un plan en especifico
    def DesafiliarProducto (self):
        try:
            
            # Buscamos si existe la afiliacion entre el producto y los planes
            # prepago
            conexion = database.operacion("","""SELECT numserie, codplan FROM ACTIVA 
            WHERE codplan = %s AND numserie = '%s'"""%(self.plan,self.producto),
            Afiliaciones.nombreBase,Afiliaciones.usuarioBase,Afiliaciones.passwordBase);
            resultado = conexion.execute()
            
            # Si no se encuentra la afiliacion entre los planes prepago
            # buscamos entre los planes postpago
            if len(resultado) == 0:
                conexion.setComando("""SELECT numserie FROM AFILIA 
                WHERE codplan = %s AND numserie = '%s'"""%(self.plan,self.producto))
                resultado = conexion.execute()
                
                # Si no se encuentra la afiliacion entre los planes postpago
                if len(resultado) == 0:
                    raise Exception("El producto ingresado no se encuentra afiliado con el plan mencionado")
                
                # Si se encuentra la afiliacion entre los planes postpago, eliminamos dicha afiliacion
                else:
                    
                    conexion.setComando("""DELETE FROM AFILIA 
                    WHERE codplan = %s AND numserie = '%s'
                    """%(self.plan,self.producto))
                    resultado = conexion.execute()
                    print 'Se ha eliminado la afiliacion exitosamente'
            
            # Si se encuentra la afiliacion entre los planes prepago, eliminamos dicha afiliacion
            else:
                conexion.setComando("""DELETE FROM ACTIVA 
                WHERE codplan = %s AND numserie = '%s'
                """%(self.plan,self.producto))
                resultado = conexion.execute()
                print 'Se ha eliminado la afiliacion exitosamente'
                
            ## Guardamos los cambios y cerramos la base de datos
            conexion.conexion.commit()
            conexion.cerrarConexion()
                    
        ## Capturamos los posibles errores.
        except Exception, e:
            print '\nERROR: ', e
            
    ## Informa a que plan o planes esta afiliado un producto
    def ConsultarPlanes (self):
        try:
            conexion = database.operacion("","""SELECT nombrepaq FROM CONTRATA 
            NATURAL JOIN PAQUETE WHERE numserie = '%s'"""%(self.producto),
            Afiliaciones.nombreBase,Afiliaciones.usuarioBase,Afiliaciones.passwordBase)
            resultado = conexion.execute()
            
            for i in resultado:
                print '\nEl producto esta asociado al paquete ' + i[0]
                
            ## Si el producto no esta asociado a ningun paquete
            if len(resultado) == 0:
                print '\nEl producto no esta afiliado a ningun paquete'
            
            conexion.setComando("""SELECT nombreplan FROM ACTIVA NATURAL JOIN 
            PLAN WHERE numserie = '%s'"""%(self.producto))
            resultado = conexion.execute()
            
            for i in resultado:
                print '\nEl producto esta asociado al plan ' + i[0]
                
            ## Si el producto no esta asociado a ningun plan prepago
            if len(resultado) == 0:
                
                conexion.setComando("""SELECT nombreplan FROM AFILIA NATURAL 
                JOIN PLAN WHERE numserie = '%s'"""%(self.producto))
                resultado = conexion.execute()
                
                for i in resultado:
                    print '\nEl producto esta asociado al plan ' + i[0]
                    
                ## Si el producto tampoco esta afiliado a planes postpago
                if len(resultado) == 0:
                    print '\nEl producto no tiene plan asociado'
                
            ## Guardamos los cambios y cerramos la base de datos
            conexion.conexion.commit()
            conexion.cerrarConexion()
            
        # Capturamos los posibles errores.
        except Exception, e:
            print '\nERROR:', e
                
    ## Elimina la afiliacion entre un producto y un paquete de servicios.
    def desafiliarContratacion(self):
        try:
            conexion = database.operacion("","""SELECT codpaq, nombrepaq FROM
            CONTRATA NATURAL JOIN PAQUETE WHERE numserie = '%s'
            """%(self.producto),Afiliaciones.nombreBase,Afiliaciones.usuarioBase,
            Afiliaciones.passwordBase)

            resultado = conexion.execute()
    
            if len(resultado) != 0:
                print "El producto esta asociado a los siguientes paquetes"

                paquetes = {}

                for row in resultado:
                    codplan = str(row[0])
                    paquetes[codplan] = row[1]
                    print codplan + ' : ' + row[1]

                entrada = ''

                while not(paquetes.has_key(entrada)):
                    entrada = str(raw_input("Por favor, introduzca el codigo del paquete que desea desafiliar\n"))

                conexion.setComando("""DELETE FROM CONTRATA WHERE codpaq = %s
                AND numserie = '%s'"""%(entrada,self.producto))
                resultado = conexion.execute()
                print ("""\nSe ha eliminado la contratacion del producto %s con el paquete %s exitosamente""")%(self.producto, entrada)

                ## Cerramos y guardamos los cambios
                conexion.conexion.commit()
                conexion.cerrarConexion()

            else:
                print "El producto no tiene paquetes asociados\n"
                
        except Exception, e:
            print '\nERROR: ', e

def impPlanyPaquetes(idProducto):
        conexion = database.operacion("",
                                """SELECT * FROM producto WHERE numserie = \'%s\'""" % idProducto,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)

        if len(conexion.execute()) == 0:
            raise Exception("El producto ingresado no existe en la base de datos")
        
        conexion = database.operacion("",
                                """SELECT codplan FROM afilia WHERE numserie = \'%s\'""" % idProducto,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)

        resultado = conexion.execute()

        if len(resultado) == 0:
            conexion = database.operacion("",
                                    """SELECT codplan FROM activa WHERE numserie = \'%s\'""" % idProducto,
                                    dbparams.dbname,dbparams.dbuser,dbparams.dbpass)

            resultado = conexion.execute()


        if len(resultado) ==0:
            raise Exception("El producto ingresado no se encuentra afiliado a ningun plan")


        codplan = resultado[0][0]

        conexion = database.operacion("",
                    """SELECT nombreplan FROM plan WHERE codplan = %s""" % codplan,
                    dbparams.dbname,dbparams.dbuser,dbparams.dbpass)

        resultado = conexion.execute()

        print "El producto esta asociado al plan " + resultado[0][0]

        conexion = database.operacion("","""select nombrepaq from contrata natural join paquete
                                            where numserie = \'%s\'""" % idProducto,
                                            dbparams.dbname,dbparams.dbuser,dbparams.dbpass)

        resultado = conexion.execute()

        print "El producto esta asociado a los siquientes paquetes: "
        for row in resultado:
            print '     ' + row[0]

## Main de pruebas
if __name__ == '__main__':
    #Afiliacion = Afiliaciones('a1',1)
    #plan = Afiliacion.buscarPlan()
    #Afiliacion = Afiliaciones ('a1',8)
    #Afiliacion.CrearAfiliacion()
    #Afiliacion = Afiliaciones('a1',10)
    #Afiliacion.CrearContratacion()
    #Afiliacion = Afiliaciones('a1',2)
    #Afiliacion.DesafiliarProducto()
    #Afiliacion = Afiliaciones('a1',1)
    #Afiliacion.ConsultarPlanes()
    Afiliacion = Afiliaciones('CBZ27326',10)
    Afiliacion.desafiliarContratacion()
    #impPlanyPaquetes("sd")