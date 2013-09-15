# Modulo menu.py
#!/usr/bin/env python
#!/usr/local/bin/python
# -*- coding: utf-8 -*-



import sys
import validacion
import moduloCliente
import productos
import consumos
import AFILIACIONES

def main():
    print("BIENVENIDOS")
   
    #Menu de las consultas
    flag = True   

    while flag:
        print "\n---Menu---"
        print "\nElija el modulo de su preferencia: "
        print "   1.- Cliente."
        print "   2.- Producto."
        print "   3.- Afiliaciones."
        print "   4.- Consumos."
        print "   5.- Empresa."
        print "   6.- Generacion de facturas."
        print "   7.- Salir"
        
        op = int(validacion.validarNumero('Opcion: '))
        
        if op == 1:
            print "\nMODULO CLIENTE"
            flag1 = True
            while flag1:                    
                print "   1.- Registrar un cliente."
                print "   2.- Consultar un cliente."
                print "   3.- Regresar al menu anterior."
        
                op1 = int(validacion.validarNumero('Opcion: '))
                if op1 == 1:
                    print "\n1.- Registrar un cliente."
                    moduloCliente.registroCliente()
                elif op1 == 2:     
                    print "\n2.- Consultar un cliente."
                    moduloCliente.consultaClientes()         
                elif op1 == 3: 
                    print "\n3.- Regresar al menu anterior."
                    flag1 = False
                elif (op1 > 3 or op1 <= 0):
                    print "\nERROR: La opcion no es valida."
                    
        elif op == 2:     
            print "\nMODULO PRODUCTO"
            flag2 = True
            producto2 = productos.Producto()
            while flag2:                    
                print "   1.- Registrar un producto."
                print "   2.- Consultar un producto."
                print "   3.- Regresar al menu anterior."
        
                op2 = int(validacion.validarNumero('Opcion: '))
                if op2 == 1:
                    print "\n1.- Registrar un producto."
                    producto2.nuevoProducto()
                elif op2 == 2:     
                    print "\n2.- Consultar un producto."
                    serie = producto2.validarSerie()                    
                    producto2.obtenerProducto(serie)        
                elif op2 == 3: 
                    print "\n3.- Regresar al menu anterior."
                    producto2.cerrarConn()
                    flag2 = False
                elif (op2 > 3 or op2 <= 0):
                    print "\nERROR: La opcion no es valida."
        elif op == 3:    
            print "\nMODULO AFILIACIONES"
            flag3 = True

            while flag3:                    
                print "   1.- Afiliar un producto."
                print "   2.- Desafiliar un producto."
                print "   3.- Regresar al menu anterior."     
                           
                op3 = int(validacion.validarNumero('Opcion: '))
                if op3 == 1:
                    print "\n1.- Afiliar un producto a un plan."
                    prod31 = productos.Producto()
                    producto31 = prod31.validarProducto()                           
                    flag31 = True                                       
                    
                    while flag31:                    
                        print "   1.- Plan."
                        print "   2.- Servicio."
                        print "   3.- Regresar."
                
                        op31 = int(validacion.validarNumero('Opcion: '))
                        if op31 == 1:
                            print "\n1.- Plan."
                            cod_plan = int(raw_input('Introduzca el codigo del plan: '))
                            Afiliacion = AFILIACIONES.Afiliaciones(producto31,cod_plan)                            
                            Afiliacion.CrearAfiliacion()
                            Afiliacion.cerrarConexion()
                            
                        elif op31 == 2:     
                            print "\n2.- Servicio."
                            cod_ser = int(raw_input('Introduzca el codigo del servicio: '))
                            Afiliacion = AFILIACIONES.Afiliaciones(producto31,cod_ser)                            
                            Afiliacion.CrearContratacion()
                            Afiliacion.cerrarConexion()
                              
                        elif op31 == 3: 
                            print "\n3.- Regresar."
                            
                            flag31 = False
                        elif (op31 > 3 or op31 <= 0):
                            print "\nERROR: La opcion no es valida."
                    producto31.cerrarConn()

                elif op3 == 2:     
                    print "\n2.- Desafiliar un producto a un plan."
                    flag32 = True
                    prod32 = productos.Producto()
                    producto32 = prod32.validarProducto()  
                    while flag32:                    
                        print "   1.- Plan."
                        print "   2.- Servicio."
                        print "   3.- Regresar."
                
                        op32 = int(validacion.validarNumero('Opcion: '))
                        if op32 == 1:
                            print "\n1.- Plan."
                            cod_plan = int(raw_input('Introduzca el codigo del plan: '))
                            Afiliacion = AFILIACIONES.Afiliaciones(producto32,cod_plan)                            
                            Afiliacion.DesafiliarProducto()
                            Afiliacion.cerrarConexion()
                            
                        elif op32 == 2:     
                            print "\n2.- Servicio."
                            cod_ser = int(raw_input('Introduzca el codigo del servicio: '))
                            Afiliacion = AFILIACIONES.Afiliaciones(producto32,cod_ser)                            
                            Afiliacion.desafiliarContratacion()
                            Afiliacion.cerrarConexion()                           
                            
                        elif op32 == 3: 
                            print "\n3.- Regresar."
                            flag32 = False
                        elif (op32 > 3 or op32 <= 0):
                            print "\nERROR: La opcion no es valida."
                    producto32.cerrarConn()
                           
                elif op3 == 3: 
                    print "\n6.- Regresar al menu anterior."                    
                    flag3 = False                    
                elif (op3 > 3 or op3 <= 0):
                    print "\nERROR: La opcion no es valida."

        elif op == 4:   
            print "\nMODULO CONSUMOS"
            flag4 = True
            while flag4:                    
                print "   1.- Registrar un consumo."
                print "   2.- Consultar consumos de un producto."
                print "   3.- Regresar al menu anterior."
        
                op4 = int(validacion.validarNumero('Opcion: '))
                if op4 == 1:
                    print "\n1.- Registrar un consumo."
                    consumos.crearConsumoInteractivo()
                elif op4 == 2:     
                    print "\n2.- Consultar consumos de un producto."       
                    consumos.consumosProducto()
                elif op4 == 3: 
                    print "\n3.- Regresar al menu anterior."
                    flag4 = False
                elif (op4 > 3 or op4 <= 0):
                    print "\nERROR: La opcion no es valida."

        elif op == 5:   
            print "\nMODULO EMPRESA"
            flag5 = True
            while flag5:                    
                print "   1.- Registrar una empresa."
                print "   2.- Consultar una empresa."
                print "   3.- Regresar al menu anterior."
        
                op5 = int(validacion.validarNumero('Opcion: '))
                if op5 == 1:
                    print "\n1.- Registrar una empresa."
                elif op5 == 2:     
                    print "\n2.- Consultar una empresa."       
                elif op5 == 3: 
                    print "\n3.- Regresar al menu anterior."
                    flag5 = False
                elif (op5 > 3 or op5 <= 0):
                    print "\nERROR: La opcion no es valida."
                    
        elif op == 6:   
            print "\nMODULO GENERACION DE FACTURAS"
            flag6 = True
            while flag6:                    
                print "   1.- Generar la factura de un cliente."
                print "   2.- Regresar al menu anterior."        
                op6 = int(validacion.validarNumero('Opcion: '))
                if op6 == 1:                    
                    print "\n1.- Generar la factura de un cliente."  
                    #Genera la factura
                elif op6 == 2: 
                    print "\n2.- Regresar al menu anterior."
                    flag6 = False
                elif (op6 > 2 or op6 <= 0):
                    print "\nERROR: La opcion no es valida."  
                                    
        elif op == 7: 
            print "\nHasta luego."
            flag = False
        elif (op > 7 or op <= 0):
            print "\nERROR: La opcion no es valida."


if __name__== "__main__":
    main()
    sys.exit()    
        
#END menu.py