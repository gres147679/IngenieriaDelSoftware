# -*- coding: utf-8 -*-
'''
Este mecanismo de pruebas está diseñado para correr en una base 
de datos aislada, que no contenga información valiosa, y que vaya 
a ser destinada únicamente para pruebas

@author: gustavo
'''
import unittest
import psycopg2
import database


class query3Test(unittest.TestCase):
    

    def setUp(self):
        self.myConsult = database.consulta(
        "Inserts de prueba para consulta 3",
        None,"ingenieria","test","123")

    def tearDown(self):
        self.myConsult.setComando("""
        delete from consume cascade;
        delete from incluye cascade;
        delete from afilia cascade;
        delete from plan_postpago cascade;
        delete from plan_prepago cascade;
        delete from plan cascade;
        delete from servicio cascade;
        delete from producto cascade;
        delete from cliente cascade;
        delete from empresa cascade;
        """)
        result = self.myConsult.execute()
        self.myConsult.cerrarConexion()

    ## Caso sin contenido en la base de datos. Debe retornar cero
    def test_casoBase(self):
        self.myConsult.setComando("select * from consulta3();")
        result = self.myConsult.execute()
        theoreticResult = 0
        self.assertEqual(result[0][0],theoreticResult,
                         "Error en la prueba 1");
        print("Prueba 1 lista")
        
    ## Caso en el que un cliente consume un servicio sin estar afiliado a un plan
    ## que lo contenga
    
    def test_unConsumoSinAfiliacion(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into plan values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into incluye values
        (3002,1001,0.1,100);
        
        insert into consume values(
        'CBZ27326',1001,current_date,50);
        
        select * from consulta3();""")
        
        
        result = self.myConsult.execute()
        theoreticResult = 0
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 2");
        print("Prueba 2 lista")
        
    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo es cubierto enteramente por el plan
    
    def test_unConsumoConAfiliacion(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONSUME values(
        'CBZ27326',1001,current_date,50);
        
        
        select * from consulta3();""")
        
        
        result = self.myConsult.execute()
        theoreticResult = 5
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 3");
        print("Prueba 3 lista")
        
        
    ## Caso en el que dos clientes consumen un servicio estando afiliados a un plan
    ## que lo contenga, y este consumo es cubierto enteramente por el plan
        
    def test_unConsumoConAfiliacionDosClientes(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into CLIENTE values (20978913,'Rebeca Machado',
        'San Antonio');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into PRODUCTO values
        ('CBZ27327','iPhone 4S','12345678',20978913);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into AFILIA values
        ('CBZ27327',3002,'paquete');
        
        insert into CONSUME values(
        'CBZ27326',1001,current_date,50);
        
        insert into CONSUME values(
        'CBZ27327',1001,current_date,50);
        
        
        select * from consulta3();""")
        
        
        result = self.myConsult.execute()
        theoreticResult = 10
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 3");
        print("Prueba 4 lista")

    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo no es cubierto enteramente por el plan,
    ## sino que parte de el es cubierto y otra parte se excede
    ##
    ## Duda: si un consumo excede la renta, debe salir en este monto?
    def test_unConsumoConAfiliacionPeroConExceso(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONSUME values(
        'CBZ27326',1001,current_date,100);
        
        
        select * from consulta3();""")
        
        
        
        result = self.myConsult.execute()
        theoreticResult = 5
        print result[0][0]
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 3");
        
        print("Prueba 5 lista")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()