import psycopg2
import psycopg2.extras
import unittest

class Factura:
    def __init__(self, idProducto):
        try:
            self.conectar = psycopg2.connect ("dbname='innova' user='gustavo' password='gustavo1994'")
            self.cur = self.conectar.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception, e:
            print "Error conectando con la base de datos. ", e                
        
        self.idProducto = idProducto
        self.nombreCliente =  self.buscarNombre()
        self.mesFacturacion = self.buscarMes()
        self.listaConsumos = self.buscarConsumos()
        self.montoTotalCobrar = self.totalCobrar()

    def buscarNombre(self):
        try:
            self.cur.execute("SELECT nombrecl FROM producto as pr, cliente as cl WHERE cl.cedula = pr.cedula and numserie = %(numserie)s",{"numserie" : self.idProducto})
            resultado = self.cur.fetchone()
            return resultado[0]
        except Exception, e:
            print "Error buscando el nombre y la direccion del cliente", e
    
    def buscarMes(self):
        return str(input("Por favor, introduzca el mes de facturacion "))
    
    def buscarConsumos(self):
        # Aqui hice un ejemplo de sustitucion de strings en python. Un poco mas sencillo que antes
        self.cur.execute("""select to_char(con.fecha, 'DD MM YYYY'), serv.nombreserv, con.cantidad, serv.codserv from consume as con, servicio as serv 
                         where con.numserie = \'%s\'  and to_number(to_char(con.fecha, 'MM'),'9999999') = %d and serv.codserv = con.codserv""" % (self.idProducto, int(self.mesFacturacion)))
        
        return self.cur.fetchall()

    def totalCobrar(self):
        self.cur.execute("SELECT codplan FROM afilia WHERE numserie = %(numserie)s",{"numserie" : self.idProducto})
        if self.cur.rowcount == 0:
            self.cur.execute("""SELECT codplan FROM activa WHERE numserie = %(numserie)s""",{"numserie" : self.idProducto})
        
        resultado = self.cur.fetchall()
        codplan = resultado[0][0]
                                
        #self.cur.execute("""select con.codserv, sum(con.cantidad) from consume as con 
                        #where con.numserie = %(numserie)s and 
                        #to_char(con.fecha, 'MM') = %(mes)s group by (con.codserv)""", 
                        #{"numserie" : self.idProducto, "mes" : self.mesFacturacion})
	self.cur.execute("""select con.codserv, sum(con.cantidad) from consume as con 
                        where con.numserie = \'%s\' and 
                        to_number(to_char(con.fecha, 'MM'),'9999999') = %d group by (con.codserv);""" % (self.idProducto,int(self.mesFacturacion)))
        totalConsumido = self.cur.fetchall()

        self.cur.execute("""select inc.codserv, inc.cantidad, inc.tarifa, serv.costo from incluye as inc, servicio as serv where inc.codplan =  %(codplan)s and serv.codserv = inc.codserv;""",
                         {"codplan" : codplan})
        
        totalPlan = self.cur.fetchall()       
         
        total = 0
        for con in totalConsumido:
            i = 0
            while i < len(totalPlan):
                if con[0] == totalPlan[i][0]:
                    limite = totalPlan[i][1]
                    consumido = con[1]
                    if consumido <= limite:
                        total = total + consumido * totalPlan[i][2]
                    else:
                        total = total + limite * totalPlan[i][2]
                        total = total + (consumido - limite) * totalPlan[i][3]
                i = i+1
        
        return total
    ## Termina la conexion con la base de datos
    def cerrarConexion(self):
        self.cur.close()
        self.conectar.close()
        
    ## Guarda los cambios realizados en la base de datos
    def guardarCambios(self):
        self.conectar.commit()

if __name__ == '__main__':
    factura = Factura("AZ622341")
    for row in factura.listaConsumos:
        print row
    
    print factura.montoTotalCobrar
    
# No considera cuando varios consumos sumados exceden el limite del plan, sino solamente si un consumo excede el limite
# Cuando un consumo esta cubierto por el plan, se cobra unicamente la renta del plan, no el valor del servicio
# No cobra la renta del plan
# No estoy seguro si considera mas de una afiliacion (caso de plan + paquete de servicios por ejemplo) que es con las relaciones contrata y contiene
# Le hace falta checkear el año de los consumos
    
