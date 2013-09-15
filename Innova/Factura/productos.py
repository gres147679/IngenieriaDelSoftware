import psycopg2
import sys
import psycopg2.extras 
 
class Producto():
    #Inicializamos la clase
    def __init__(self):
        # Colocamos las variables asi para mas rapido acceso y cambio posterior
        self.dbname = 'software'
        self.user = 'postgres'
        self.password = '18588'
        self.host = 'localhost'
        
        try:
            #Hacemos el vinculo con la base de datos
            self.conn = psycopg2.connect(host=self.host,dbname=self.dbname,user=self.user,password=self.password)
            
        except:
            print "No se pudo conectar a la base de datos"
            sys.exit()
            
    # Funcion para cerrar la conexion con la base de datos
    def cerrarConn(self):
        self.conn.close()
        
    # Funcion para pedir los datos del producto por consola    
    def pedirProducto(self):
        print "Favor rellenar los datos pedidos a continuacion: \n"
        #Se piden los datos y se validan
        numserie = self.validarSerie()
        nombre = self.validarProducto()
        rif = self.validarRIF()
        cedula = self.validarCedula()
        return(numserie,nombre,rif,cedula)
        
    #Validamos el numero de serie introducido por consola
    def validarSerie(self):
        #Numero de Serie (CLAVE)
        while True:
            while True:
                numserie = raw_input('Numero de Serie: ')
                #Verifica que sea distinto de una cadena vacia
                if (numserie == ""):
                    print "\n ERROR: Entrada no valida."
                    continue
                print ("El numero de serie es: " + numserie + " ?\n")
                respuesta = raw_input("Es correcto?: [s/n]   ")
                if (respuesta.lower() != 'n'):
                    break
                else:
                    continue
            break
        return numserie
        
    #Validamos el nombre del producto introducido por consola
    def validarProducto(self):
        #Nombre del Producto
        while True:
            while True:
                nombre = raw_input('Nombre del Producto: ')
                #Verifica que sea distinto de una cadena vacia
                if (nombre == ""):
                    print "\n ERROR: Entrada no valida."
                    continue
                print ("El nombre de su producto es: " + nombre + " ?\n")
                respuesta = raw_input("Es correcto?: [s/n]   ")
                if (respuesta.lower() != 'n'):
                    break
                
            break 
        return nombre
        
    #Validamos el RIF  introducido por consola
    def validarRIF(self):
        #RIF
        while True:
            try:
                y = int(raw_input('RIF: '))
            except ValueError:
                print "/n ERROR: Se debe ingresar un numero entero \n"
            else:
                if (y <= 0):
                    print "\n ERROR: El numero debe ser positivo\n"
                rif = str(y)
                break
        return rif
        
    #Validamos el numero de cedula introducido por consola
    def validarCedula(self):
        #Cedula
        while True:
            try:
                x = int(raw_input('cedula: '))
            except ValueError:
                print "/n ERROR: Se debe ingresar un numero entero \n"
            else:
                if (x <= 0):
                    print "\n ERROR: El numero debe ser positivo\n"
                cedula = str(x)
                break
        return cedula
        
    # Funcion que nos permite agregar nuevos productos a la base de datos
    def nuevoProducto(self):
        cursor = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        
        producto = self.pedirProducto()
        #El excute se hace de una con el paso de parametros para evitar el SQL Inyection
        cursor.execute("INSERT INTO PRODUCTO (numserie,nombreprod,RIF,cedula) VALUES (%s,%s,%s,%s);",producto)
        print ("Se ha agregado el producto con los siguientes valores %s %s %s %s \n" % producto)
        #Se usa el commit para guardar los cambios realizados en la base de datos
        self.conn.commit()
        cursor.close()
        
    # Funcion que elimina un producto de la base de datos.Recibe de parametro de entrada el numero de serie
    # del producto a eliminar
    def eliminarProducto(self,nserie):
        cursor = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute("DELETE FROM PRODUCTO WHERE numserie=%(nserie)s",{'nserie' : nserie})
        self.conn.commit()
        cursor.close()
        
    # Verifica la cantidad de productos agregados a la base de datos    
    def cantidadProductos (self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT COUNT(*) FROM PRODUCTO")
        x=cursor.fetchone()
        resultado = x[0]
        cursor.close()
        #print resultado
        return (resultado)
        
    # Funcion que nos permite saber si un producto existe en la base de datos
    # Recibe de entrada el numero de serie del producto a buscar
    def buscarProducto(self,nserie):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT COUNT(*) FROM PRODUCTO WHERE numserie = %(nserie)s",{'nserie' : nserie})
        x=cursor.fetchone()
        resultado = x[0]
        cursor.close()
        return (resultado > 0)
    # Funcion que nos devuelve el producto buscado.
    # Recibe de entrada el numero de serie del producto en cuestion.
    
    def obtenerProducto(self,nserie):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  
        producto = None
        if (self.cantidadProductos() == 0):
            print "\n Error: La base de datos esta vacia"
        else:
            if (self.buscarProducto(nserie)):
                cursor.execute("SELECT * from PRODUCTO WHERE numserie = %(nserie)s",{'nserie' : nserie})
                for row in cursor.fetchall():
                    writeRow = 'Numero de Serie: ' + str(row['numserie'])
                    writeRow += ' Nombre: ' + str(row['nombreprod'])
                    writeRow += ' RIF: ' + str(row['rif'])
                    writeRow += ' Cedula: ' + str(row['cedula'])
                    print writeRow
        return writeRow
        
      ##### MAIN #####
#if __name__ == "__main__":

#    producto2 = Producto()
    #producto2.pedirProducto()
    #producto2.eliminarProducto('123')
#    print producto2.cantidadProductos()
#    print producto2.buscarProducto('p1223')
#    producto2.obtenerProducto('p123')
    
    #### END MAIN ####