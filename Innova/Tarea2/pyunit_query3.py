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
        self.listaTuplas = []
        self.myConsult = database.consulta(
        "Inserts de prueba para consulta 3",
        None,"ingenieria","test","123")

    def tearDown(self):
        del self.listaTuplas


    def test_casoBase(self):
        self.myConsult.setComando("select * from consulta3();")
        result = self.myConsult.execute()
        theoreticResult = 0
        print type(result[0][0])
        self.assertEqual(result[0][0],theoreticResult,"Error en la prueba 1");
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()