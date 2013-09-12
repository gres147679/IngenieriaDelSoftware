# -*- coding: utf-8 -*-
#!/usr/bin/python

import unittest
import psycopg2
import database

class query4Test(unittest.TestCase):
    # Parametros de conexion de la base de datos
    dbname = "ingenieria"
    dbuser = "gustavo"
    dbpass = "12345"
    
    def setUp(self):
        self.myConsult = database.consulta(
        "Inserts de prueba para consulta 4",
        None,self.dbname,self.dbuser,self.dbpass)

    def tearDown(self):
        self.myConsult.setComando("""
        delete from consume cascade;
        delete from incluye cascade;
        delete from activa cascade;
        delete from contiene cascade;
        delete from contrata cascade;
        delete from servicio cascade;
        delete from paquete cascade;
        delete from plan_postpago cascade;
        delete from plan_prepago cascade;
        delete from plan cascade;
        delete from producto cascade;
        delete from cliente cascade;
        delete from empresa cascade;
        """)
        result = self.myConsult.execute()
        self.myConsult.cerrarConexion()

    ## Caso sin contenido en la base de datos. Debe retornar cero
    def test_casoBase(self):
        self.myConsult.setComando("select * from consulta4();")
        result = self.myConsult.execute()
        theoreticResult = 0
        self.assertEqual(result[0][0],theoreticResult,
                        "Error en la prueba 1 (la BD esta vacia)");
        print("Prueba 1 lista")
        
        
    ## Caso en que hay productos pero sin activar un plan. Debe retornar 0
    def test_ningunaActivacion(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into plan values
        (3001,'MOCEL 2000','Este fabuloso plan incluye 
        segundos a cualquier telefono, SMS y buzón de
        mensajes',49,149,'prepago');
        
        select * from consulta4();""")
        
        result = self.myConsult.execute()
        theoreticResult = 0
        self.assertEqual(result[0][0],theoreticResult,
            "Error en la prueba 2 (no hay plan activado)");
        print("Prueba 2 lista")
        
        
    ## Caso en el que un cliente consume un servicio sin estar afiliado a un
    ## plan que lo contenga
    def test_unConsumoSinActivacion(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values 
        (1005,'Buzón msj',13.5,TRUE);
        
        insert into plan values
        (3001,'MOCEL 2000','Este fabuloso plan incluye 
        segundos a cualquier teléfono, SMS y buzón de
        mensajes',49,149,'prepago');
        
        insert into consume values(
        'CBZ27326',1005,current_date,1);
        
        select * from consulta4();""")
        
        result = self.myConsult.execute()
        theoreticResult = 0
        self.assertEqual(result[0][0],theoreticResult,
            "Error en la prueba 3 (no hay un plan activado)");
        print("Prueba 3 lista")
        
            
    ## Caso en que un cliente activa el mismo plan prepago con productos
    ## distintos
    def test_dosProductosActivados(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'TVCABLE');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('A001','Decodificador','12345678',22714709);
        
        insert into PRODUCTO values
        ('A002','Decodificador','12345678',22714709);
        
        insert into plan values
        (3001,'TVCABLE Bronce','...',140,150,'prepago');
        
        insert into plan values
        (3003,'TVCABLE Plata','...',220,250,'prepago');
        
        insert into SERVICIO values 
        (1001,'Canal Nacional',0,FALSE);

        insert into SERVICIO values 
        (1002,'Canal de Variedades',0,FALSE);
        
        insert into incluye values
        (3001,1001,0.1,14);

        insert into incluye values
        (3001,1002,0.23,15);

        insert into incluye values
        (3003,1001,0.14,14);

        insert into incluye values
        (3003,1002,0.12,28);
        
        insert into ACTIVA values
        ('A001',3001,0);
        
        insert into ACTIVA values
        ('A002',3003,0);
        
        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 10.17
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 4");
        print("Prueba 4 lista")        
    
    
    ## Caso en que dos clientes activan un plan prepago distinto
    def test_dosClientesActivanPlanDistinto(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'TVCABLE');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
        
        insert into CLIENTE values
        (20978913,'Rebeca Machado','San Antonio');
        
        insert into PRODUCTO values
        ('A004','Decodificador','12345678',22714709);

        insert into PRODUCTO values
        ('A005','Decodificador','12345678',20978913);
        
        insert into plan values
        (3001,'TVCABLE Bronce','...',140,150,'prepago');
        
        insert into plan values
        (3003,'TVCABLE Plata','...',220,250,'prepago');
        
        insert into SERVICIO values 
        (1001,'Canal Nacional',0,FALSE);

        insert into SERVICIO values 
        (1002,'Canal de Variedades',0,FALSE);
        
        insert into incluye values
        (3001,1001,0.1,14);

        insert into incluye values
        (3001,1002,0.23,15);

        insert into incluye values
        (3003,1001,0.14,14);

        insert into incluye values
        (3003,1002,0.12,28);
        
        insert into ACTIVA values
        ('A004',3001,0);
        
        insert into ACTIVA values
        ('A005',3003,0);
        
        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 10.17
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 5");
        print("Prueba 5 lista")
        
        
    ## Caso en que un cliente hace el consumo de una parte de lo que incluye su
    ## plan
    def test_unConsumoIncluido(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
    
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);

        insert into SERVICIO values 
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into SERVICIO values 
        (1002,'Segundos otras oper',0.3,FALSE);
        
        insert into plan values
        (3001,'MOCEL 2000','Este fabuloso plan incluye segundos a cualquier
        teléfono, SMS y buzón de mensajes',49,149,'prepago');
                  
        insert into INCLUYE values
        (3001,1001,0.15,1000);

        insert into INCLUYE values
        (3001,1002,0.3,1000);
        
        insert into ACTIVA values
        ('CBZ27326',3001,0);
        
        insert into CONSUME values
        ('CBZ27326',1001,CURRENT_DATE,50);
        
        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 442.5
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 6");
        print("Prueba 6 lista")
    
    
    ## Un cliente consume más de lo que incluye su plan con saldo suficiente
    def test_unConsumoNoIncluido(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
    
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);

        insert into SERVICIO values 
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into SERVICIO values 
        (1002,'Segundos otras oper',0.3,FALSE);
        
        insert into plan values
        (3001,'MOCEL 2000','Este fabuloso plan incluye segundos a cualquier
        teléfono, SMS y buzón de mensajes',49,149,'prepago');
                  
        insert into INCLUYE values
        (3001,1001,0.15,1000);

        insert into INCLUYE values
        (3001,1002,0.3,1000);
        
        insert into ACTIVA values
        ('CBZ27326',3001,10);
        
        insert into CONSUME values
        ('CBZ27326',1001,CURRENT_DATE,1005);
        
        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 300
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 7");
        print("Prueba 7 lista")
        
        
    ## Un cliente consume todos los servicios de su plan y ésta es la única
    ## afiliacion
    def test_unConsumoCompleto(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
    
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);

        insert into SERVICIO values 
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into SERVICIO values 
        (1002,'Segundos otras oper',0.3,FALSE);
        
        insert into plan values
        (3001,'MOCEL 2000','Este fabuloso plan incluye segundos a cualquier
        teléfono, SMS y buzón de mensajes',49,149,'prepago');
                  
        insert into INCLUYE values
        (3001,1001,0.15,1000);

        insert into INCLUYE values
        (3001,1002,0.3,1000);
        
        insert into ACTIVA values
        ('CBZ27326',3001,10);
        
        insert into CONSUME values
        ('CBZ27326',1001,CURRENT_DATE,1000);
        
        insert into CONSUME values
        ('CBZ27326',1002,CURRENT_DATE,1000);
        
        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 0
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 8");
        print("Prueba 8 lista")  
        
        
    ## Dos clientes consumen el mismo servicio con dos productos distintos, sin
    ## excederse de su plan
    def test_dosClientesConsumoIncompleto(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
        
        insert into CLIENTE values
        (20978913,'Rebeca Machado','San Antonio');
    
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into PRODUCTO values
        ('CBZ27327','iPhone 5','12345678',22714709);

        insert into SERVICIO values 
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into SERVICIO values 
        (1002,'Segundos otras oper',0.3,FALSE);
        
        insert into PLAN values
        (3001,'MOCEL 2000','Este fabuloso plan incluye segundos a cualquier
        teléfono, SMS y buzón de mensajes',49,149,'prepago');
                  
        insert into INCLUYE values
        (3001,1001,0.15,1000);

        insert into INCLUYE values
        (3001,1002,0.3,1000);
        
        insert into ACTIVA values
        ('CBZ27326',3001,10);
        
        insert into ACTIVA values
        ('CBZ27327',3001,10);
        
        insert into CONSUME values
        ('CBZ27326',1001,CURRENT_DATE,500);
        
        insert into CONSUME values
        ('CBZ27326',1001,TO_DATE('2013-06-04','YYYY-MM-DD'),100);
        
        insert into CONSUME values
        ('CBZ27327',1002,CURRENT_DATE,500);
        
        insert into CONSUME values
        ('CBZ27327',1001,CURRENT_DATE,250);
        
        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 622.5
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 9");
        print("Prueba 9 lista")
        
        
    # Dos clientes que consumen completamente los servicios de sus planes
    def test_dosClientesConsumoTotal(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
        
        insert into CLIENTE values
        (20978913,'Rebeca Machado','San Antonio');
    
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into PRODUCTO values
        ('CBZ27327','iPhone 5','12345678',22714709);

        insert into SERVICIO values 
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into SERVICIO values 
        (1002,'Segundos otras oper',0.3,FALSE);
        
        insert into PLAN values
        (3001,'MOCEL 2000','Este fabuloso plan incluye segundos a cualquier
        teléfono, SMS y buzón de mensajes',49,149,'prepago');
                  
        insert into INCLUYE values
        (3001,1001,0.15,1000);

        insert into INCLUYE values
        (3001,1002,0.3,1000);
        
        insert into ACTIVA values
        ('CBZ27326',3001,10);
        
        insert into ACTIVA values
        ('CBZ27327',3001,10);
        
        insert into CONSUME values
        ('CBZ27326',1001,CURRENT_DATE,500);
        
        insert into CONSUME values
        ('CBZ27326',1001,TO_DATE('2013-06-04','YYYY-MM-DD'),500);
        
        insert into CONSUME values
        ('CBZ27326',1002,CURRENT_DATE,500);
        
        insert into CONSUME values
        ('CBZ27326',1002,TO_DATE('2013-06-04','YYYY-MM-DD'),500);
        
        insert into CONSUME values
        ('CBZ27327',1001,CURRENT_DATE,200);
        
        insert into CONSUME values
        ('CBZ27327',1001,TO_DATE('2013-06-04','YYYY-MM-DD'),200);
        
        insert into CONSUME values
        ('CBZ27327',1001,TO_DATE('2013-06-03','YYYY-MM-DD'),600);
        
        insert into CONSUME values
        ('CBZ27327',1002,CURRENT_DATE,1000);
        
        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 0
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 10");
        print("Prueba 10 lista")
        
        
    # Consumos de un cliente en meses distintos (debe dar solo lo debido en el
    # mes actual)
    def test_dosConsumosMesesDistintos(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);

        insert into SERVICIO values 
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into PLAN values
        (3001,'MOCEL 2000','Este fabuloso plan incluye segundos a cualquier
        teléfono, SMS y buzón de mensajes',49,149,'prepago');
                  
        insert into INCLUYE values
        (3001,1001,0.15,1000);

        insert into ACTIVA values
        ('CBZ27326',3001,10);

        insert into CONSUME values
        ('CBZ27326',1001,CURRENT_DATE,500);
        
        insert into CONSUME values
        ('CBZ27326',1001,TO_DATE('2013-05-04','YYYY-MM-DD'),500);
        
        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 75
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 11");
        print("Prueba 11 lista")
        
        
    ## Un cliente se afilia a un plan que incluye cierto servicio y contrata un
    ## pquete con el mismo servicio (debe contar solo lo del plan)
    def test_clienteContrataPaquete(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);

        insert into SERVICIO values 
        (1004,'Mensajes de texto',0.35,FALSE);
        
        insert into PLAN values
        (3001,'MOCEL 2000','Este fabuloso plan incluye segundos a cualquier
        teléfono, SMS y buzón de mensajes',49,149,'prepago');
        
        insert into paquete values
        (4001,'Pegadito con otros 1500',16);
        
        insert into incluye values
        (3001,1004,0.35,200);
        
        insert into contiene values
        (4001,1004,800);
                 
        insert into ACTIVA values
        ('CBZ27326',3001,10);

        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 70
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 12");
        print("Prueba 12 lista")
        
        
    ## Un cliente consume un servicio incluido en su plan y además contrata un
    ## paquete del mismo servicio (debe descontar de la deuda)
    def test_clienteContrataPaqueteyConsume(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values
        (22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);

        insert into SERVICIO values 
        (1004,'Mensajes de texto',0.35,FALSE);
        
        insert into PLAN values
        (3001,'MOCEL 2000','Este fabuloso plan incluye segundos a cualquier
        teléfono, SMS y buzón de mensajes',49,149,'prepago');
        
        insert into paquete values
        (4001,'Pegadito con otros 1500',16);
        
        insert into incluye values
        (3001,1004,0.35,200);
        
        insert into contiene values
        (4001,1004,800);
                 
        insert into ACTIVA values
        ('CBZ27326',3001,10);
        
        insert into CONSUME values
        ('CBZ27326',1004,CURRENT_DATE,30);

        select * from consulta4();
        """)
        
        result = self.myConsult.execute()
        theoreticResult = 59.5
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 13");
        print("Prueba 13 lista")
        
    
if __name__ == "__main__":
    unittest.main()