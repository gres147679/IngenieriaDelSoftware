-- Sección de la empresa
insert into EMPRESA values
(12345678,'MOCEL');

-- Sección de clientes
insert into CLIENTE values
(22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');

insert into CLIENTE values
(20978913,'Rebeca Machado','San Antonio, Los Teques');

insert into CLIENTE values
(21205002,'Paul Baptista','Urb. Monte Monte Elena Qta. La Niebla');

insert into CLIENTE values
(21205003,'Victor Sanchez','Urb. Monte Monte Elena Qta. La Niebla');

insert into CLIENTE values
(21205004,'Fabio Castro','Urb. El Placer');

insert into CLIENTE values
(21205005,'Catherine Lollett','Los Guayabitos');

insert into CLIENTE values
(21205006,'Roberto Goncalves','Urb. Monte Elena Qta. Santa Teresa');

insert into CLIENTE values
(21205007,'Marina Salas','Petare');

insert into CLIENTE values
(21205008,'Yohnaikel Mendoze','Las Minas de Baruta');

insert into CLIENTE values
(21205009,'Caren Lengster','La Lagunita');

insert into CLIENTE values
(21205010,'Juan Perez','Maracacuay');

insert into CLIENTE values
(21205011,'Victor de Ponte','Las Mercedes');

insert into CLIENTE values
(21205012,'Lisset Herrera','Charallave');

insert into CLIENTE values
(21205013,'Juan Pobre','Cartanal');

insert into CLIENTE values
(21205014,'Andrea Medina','Quinta Crespo');

insert into CLIENTE values
(21205015,'Karla Vera','Chacao');

insert into CLIENTE values
(21205016,'Victoria Guerra','Cua');

insert into CLIENTE values
(21205017,'Andres Benitez','Catia');

insert into CLIENTE values
(21205018,'Maickel Suarez','Las Minas de Baruta');

insert into CLIENTE values
(21205019,'Pedro Lengster','La Lagunita');


-- Sección de los equipos
insert into PRODUCTO values
('CBZ27326','iPhone 4S','12345678',22714709);

insert into PRODUCTO values
('CBZ27327','iPhone 5','12345678',22714709);

insert into PRODUCTO values
('AZ622341','BlackBerry Z10','12345678',20978913);

insert into PRODUCTO values
('AZ622342','BlackBerry Z10','12345678',21205002);

-- Sección de servicios 
insert into SERVICIO values 
(1001,'Segundos a MOCEL',0.15,FALSE);

insert into SERVICIO values 
(1002,'Segundos otras oper',0.3,FALSE);

insert into SERVICIO values 
(1003,'Segundos a fijos',0.2,FALSE);

insert into SERVICIO values 
(1004,'Mensajes de texto',0.35,FALSE);

insert into SERVICIO values 
(1005,'Buzón msj',13.5,TRUE);

insert into SERVICIO values 
(1006,'Seg cualquier oper',0.2,FALSE);

-- Sección de planes
insert into plan values
(3001,'MOCEL 2000','Este fabuloso plan incluye segundos a cualquier teléfono, SMS y buzón de mensajes',49,149,'prepago');

insert into plan values
(3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y tarifas para excesos',211,311,'postpago');

-- Sección de Paquetes
insert into paquete values
(4001,'Pegadito con otros 1500',16);

insert into paquete values
(4002,'Pegadito con otros 30',19);

insert into paquete values
(4003,'Mensajes 800',38);

-- Sección de servicios para planes

-- Servicios incluidos para el plan Mocel 2000
insert into incluye values
(3001,1001,0.15,1000);

insert into incluye values
(3001,1002,0.3,1000);

insert into incluye values
(3001,1004,0.35,200);

insert into incluye values
(3001,1005,13.5,1);

-- Servicios incluidos para el plan Mixto Plus
insert into incluye values
(3002,1001,0.01150,39000);

insert into incluye values
(3002,1002,0.01250,2600);

insert into incluye values
(3002,1003,0.01150,5000);

insert into incluye values
(3002,1004,0.35,200);

insert into incluye values
(3002,1005,13.5,1);

-- Sección de servicios para paquetes

-- Servicios incluidos para el paquete pegadito con otros 1500
insert into contiene values
(4001,1006,1500);

-- Servicios incluidos para el paquete pegadito con otros 300
insert into contiene values
(4002,1006,1800);

-- Servicios incluidos para el paquete mensajes 800
insert into contiene values
(4001,1004,800);

-- Afiliaciones
insert into ACTIVA values
('CBZ27326',3001,0);

insert into AFILIA values
('CBZ27327',3002,'paquete');

insert into AFILIA values
('AZ622341',3002,'paquete');

insert into CONTRATA values
('AZ622341',4001);

insert into AFILIA values
('AZ622342',3002,'paquete');
