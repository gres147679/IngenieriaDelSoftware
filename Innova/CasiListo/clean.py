import dbparams
import database

dbname = dbparams.dbname
dbuser = dbparams.dbuser
dbpass = dbparams.dbpass

myConsult = database.operacion(
"Inserts de prueba para probar la factura",
None,dbname,dbuser,dbpass)

myConsult.setComando("""
delete from consume cascade;
delete from incluye cascade;
delete from afilia cascade;
delete from plan_postpago cascade;
delete from plan_prepago cascade;
delete from plan cascade;
delete from contiene cascade;
delete from servicio cascade;
delete from contrata cascade;
delete from paquete cascade;
delete from producto cascade;
delete from cliente cascade;
delete from empresa cascade;
""")
result = myConsult.execute()
myConsult.cerrarConexion()