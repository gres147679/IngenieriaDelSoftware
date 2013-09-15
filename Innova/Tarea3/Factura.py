# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
import unittest

class Factura:
    def __init__(self, idProducto):
        try:
            self.conectar = psycopg2.connect ("dbname='tarea' user='jljb1990' password=''")
            self.cur = self.conectar.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception, e:
            print "Error conectando con la base de datos. ", e                
        
        self.idProducto = idProducto
        self.nombreCliente =  self.buscarNombre()
        self.mesFacturacion = self.buscarMes()
        self.anioFacturacion = self.buscarAnio()
        self.listaConsumos = self.buscarConsumos()
        self.montoTotalCobrar = self.totalCobrar()

    def buscarNombre(self):
        try:
            self.cur.execute("SELECT nombrecl FROM producto as pr, cliente as cl WHERE cl.cedula = pr.cedula and numserie = %(numserie)s",
                             {"numserie" : self.idProducto})
            resultado = self.cur.fetchone()
            return resultado[0]
        except Exception, e:
            print "Error buscando el nombre y la direccion del cliente", e
    
    def buscarMes(self):
        return str(raw_input("Por favor, introduzca el mes de facturacion "))
    
    def buscarAnio(self):
        return str(input("Por favor, introduzca el año de facturacion "))

    def buscarConsumos(self):
        # Aqui hice un ejemplo de sustitucion de strings en python. Un poco mas sencillo que antes
        self.cur.execute("""select to_char(con.fecha, 'DD MM YYYY'), serv.nombreserv, con.cantidad, serv.codserv from consume as con, servicio as serv 
                         where con.numserie = \'%s\'  and to_number(to_char(con.fecha, 'MM'),'9999999') = %d and serv.codserv = con.codserv""" % (self.idProducto, int(self.mesFacturacion)))
        
        return self.cur.fetchall()

    def totalCobrar(self):
        #Buscamos el codigo del plan asociado al producto
        self.cur.execute("SELECT codplan FROM afilia WHERE numserie = %(numserie)s",{"numserie" : self.idProducto})
        if self.cur.rowcount == 0:
            self.cur.execute("""SELECT codplan FROM activa WHERE numserie = %(numserie)s""",{"numserie" : self.idProducto})
        
        resultado = self.cur.fetchall()
        codplan = resultado[0][0]
        
        #------------------------------------------------------------------------------------------------------------------------
        #Buscamos la renta del plan que se va a cobrar al producto.
        
        self.cur.execute("""SELECT renta_basica FROM plan WHERE codplan = %(codplan)s""",{"codplan" : codplan})
        resultado = self.cur.fetchall()
        renta = int(resultado[0][0])
        
        #------------------------------------------------------------------------------------------------------------------------
        #Buscamos la suma de todos los consumos por servicio hechos por el producto en el año y mes introducidos por el usuario. Lo guardamos en un
        #diccionario donde la clave es el codigo del servicio.
        self.cur.execute("""select con.codserv, sum(con.cantidad) as total from consume as con 
                        where con.numserie = %(numserie)s and 
                        to_char(con.fecha, 'MM YYYY') = %(mesAnio)s group by (con.codserv)""", 
                        {"numserie" : self.idProducto, "mesAnio" : self.mesFacturacion + " " + self.anioFacturacion})

        #self.cur.execute("""select con.codserv, sum(con.cantidad) as total from consume as con 
                        #where con.numserie = \'%s\' and 
                        #to_number(to_char(con.fecha, 'MM'),'9999999') = %d group by (con.codserv);""" % (self.idProducto,int(self.mesFacturacion)))
        resultado = self.cur.fetchall()
        
        totalConsumido = {}
        for row in resultado:
                totalConsumido[row["codserv"]] = int(row["total"])
        
        print totalConsumido.items()
        
        #-----------------------------------------------------------------------------------------------------------------------------
        #Buscamos los servicios ofrecidos por el plan y la cantidad y tarifa ofrecidos por este. El resultado se guarda en un diccionario
        #donde la clave es el codigo del servicio.
        self.cur.execute("""select inc.codserv, inc.cantidad, inc.tarifa from incluye as inc, servicio as serv 
                         where inc.codplan =  %(codplan)s and serv.codserv = inc.codserv;""",
                         {"codplan" : codplan})
        
        resultado = self.cur.fetchall()       
         
        totalPlan = {}
        
        for row in resultado:
            totalPlan[row["codserv"]] = [row["cantidad"], row["tarifa"]]
        
        
        #print totalPlan.items()
        
        #---------------------------------------------------------------------------------------------------------------------------------
        #Se busca si el producto este asociado a algun paquete. De estarlo, las cantidades de servicio ofrecidas se agregan al
        #diccionario de los servicios ofrecidos por el plan.
        self.cur.execute("""SELECT codserv, cantidad, costo from contrata natural join contiene natural join servicio 
                         where numserie = %(numserie)s""",{ "numserie" : self.idProducto})
        
        resultado = self.cur.fetchall()
        for row in resultado:
            codserv = row["codserv"]
            if totalPlan.has_key(codserv):
                totalPlan[codserv][0] = totalPlan[codserv][0] + int(row["cantidad"])
            else:
                totalPlan[codserv] = [int(row["cantidad"]), row["costo"]]
        
        print totalPlan.items()
        
        #---------------------------------------------------------------------------------------------------------------------
        #Se busca el costo total de todos los paquetes a los que esta suscrito el producto. El resultado se almacena
        #en el total a cobrar.
        self.cur.execute("""select sum(precio) from contrata natural join paquete 
                         where numserie = %(numserie)s group by(contrata.numserie)""", { "numserie" : self.idProducto})
        
        if self.cur.rowcount == 0:
            total = 0
        else:
            total = int(self.cur.fetchall()[0][0])
        
        #---------------------------------------------------------------------------------------------------------------------
        #Se verifica la suma de los consumos por servicio del producto, si excede el valor ofrecido por el plan/paquete
        #entonces se cobra lo indicado por el plan. En caso que el serivicio sea ofrecido por un paquete, se cobra por exceso
        #el costo del servicio.
        for con in totalConsumido.keys():
            consumido = totalConsumido[con]
            limite = totalPlan[con][0]
            if consumido > limite:
                total = total + (consumido - limite) * totalPlan[con][1]
        
        return total + renta

    ## Termina la conexion con la base de datos
    def cerrarConexion(self):
        self.cur.close()
        self.conectar.close()

if __name__ == '__main__':
    factura = Factura("CBZ27326")
    #for row in factura.listaConsumos:
        #print row
    
    print factura.montoTotalCobrar
    
# No considera cuando varios consumos sumados exceden el limite del plan, sino solamente si un consumo excede el limite. LISTO.
# Cuando un consumo esta cubierto por el plan, se cobra unicamente la renta del plan, no el valor del servicio.LISTO.
# No cobra la renta del plan.LISTO.
# No estoy seguro si considera mas de una afiliacion (caso de plan + paquete de servicios por ejemplo) que es con las relaciones contrata y contiene.LISTO.
# Le hace falta checkear el año de los consumos.LISTO.