/*
Triggers que se encargan de la segunda restricción explícita:
2. Si un servicio es único, el atributo cantidad en cada instancia de las
interrelaciones consume, contiene e incluye debe valer 1
*/


CREATE OR REPLACE FUNCTION servicioEsUnico1() 
RETURNS TRIGGER AS $servicioEsUnico1$
  BEGIN
    IF (SELECT unico 
    FROM SERVICIO AS origen 
    WHERE origen.codserv=NEW.codserv) THEN
      IF NEW.cantidad = 1 AND NOT EXISTS (select * from CONSUME AS origen 
      where origen.numSerie = NEW.numSerie AND origen.codserv = NEW.codserv)
	THEN RETURN NEW;
	ELSE RETURN NULL;
      END IF;
    END IF;
    RETURN NEW;
  END;
$servicioEsUnico1$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION servicioEsUnico2() 
RETURNS TRIGGER AS $servicioEsUnico2$
  BEGIN
    IF (SELECT unico 
    FROM SERVICIO AS origen 
    WHERE origen.codserv=NEW.codserv) THEN
      IF NEW.cantidad = 1 AND NOT EXISTS(select * from INCLUYE AS 
      origen where origen.codserv = NEW.codserv AND origen.codplan = NEW.codplan)
      THEN RETURN NEW;
      ELSE RETURN NULL;
      END IF;
    END IF;
    RETURN NEW;
  END;
$servicioEsUnico2$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION servicioEsUnico3() 
RETURNS TRIGGER AS $servicioEsUnico3$
  BEGIN
    IF (SELECT unico 
    FROM SERVICIO AS origen 
    WHERE origen.codserv=NEW.codserv) THEN
      IF NEW.cantidad = 1 AND NOT EXISTS(select * from CONTIENE AS 
      origen where origen.codpaq = NEW.codpaq AND origen.codserv = NEW.codserv)
      THEN RETURN NEW;
      ELSE RETURN NULL;
      END IF;
    END IF;
    RETURN NEW;
  END;
$servicioEsUnico3$ LANGUAGE plpgsql;
  
CREATE TRIGGER servicioEsUnico1 
BEFORE INSERT OR UPDATE ON CONSUME FOR EACH ROW 
EXECUTE PROCEDURE servicioEsUnico1();

CREATE TRIGGER servicioEsUnico2 
BEFORE INSERT OR UPDATE ON INCLUYE FOR EACH ROW 
EXECUTE PROCEDURE servicioEsUnico2();

CREATE TRIGGER servicioEsUnico3 
BEFORE INSERT OR UPDATE ON CONTIENE FOR EACH ROW 
EXECUTE PROCEDURE servicioEsUnico3();


-- Trigger que actualiza el saldo prepago

CREATE OR REPLACE FUNCTION actualizaSaldo() 
RETURNS TRIGGER AS $actualizaSaldo$
DECLARE
  costoServ integer;
  saldoAf integer;
  canti integer;
  incluido integer;
  porpaquete integer;
  BEGIN
    porpaquete = (select cantidad from paquete natural join contiene where codserv=NEW.codserv);
    if porpaquete is null then porpaquete = 0; end if;
    
    canti = (select sum(cantidad) from consume where codserv=NEW.codserv and numserie = NEW.numserie
    and to_number(to_char(fecha,'MM'),'9999999')=to_number(to_char(NEW.fecha,'MM'),'9999999') 
    and to_number(to_char(fecha,'YYYY'),'9999999')=to_number(to_char(NEW.fecha,'YYYY'),'9999999') );
    if canti is null then canti = 0; end if;
    
    incluido = (select cantidad from incluye where codserv = NEW.codserv and codplan =
    (select codplan from activa where numserie = NEW.numserie));
    if incluido is null then incluido = 0; end if;
    
    costoServ = (select costo from servicio where codserv=NEW.codserv);
    saldoAf = (select saldo from activa where numserie = NEW.numserie);
    if NEW.cantidad > (incluido+porpaquete-canti) THEN 
      update activa set saldo = (saldoAf-(NEW.cantidad-incluido+canti))*costoServ where numserie = NEW.numserie;      
    else
      return null;
    END if;
    return NEW;
    
  END;  
$actualizaSaldo$ LANGUAGE plpgsql;

CREATE TRIGGER actualizaSaldo 
AFTER INSERT ON CONSUME FOR EACH ROW 
EXECUTE PROCEDURE actualizaSaldo();

-- Trigger que auto-crea el paquete
CREATE OR REPLACE FUNCTION autoCreaPaquete() 
RETURNS TRIGGER AS $autoCreaPaquete$
DECLARE
  costoServ integer;
  saldoAf integer;
  canti integer;
  incluido integer;
  BEGIN
    IF (NEW.unico) THEN
      INSERT INTO PAQUETE VALUES
      (NEW.codserv,'Paquete ' || NEW.nombre,NEW.costo);
      INSERT INTO CONTIENE VALUES
      (NEW.codserv,NEW.codserv,1);
    END IF;
    RETURN NEW;
  END;  
$autoCreaPaquete$ LANGUAGE plpgsql;

CREATE TRIGGER autoCreaPaquete
AFTER INSERT ON SERVICIO FOR EACH ROW 
EXECUTE PROCEDURE autoCreaPaquete();

-- Trigger que verifica tarifas no nulas
CREATE OR REPLACE FUNCTION tarifasNulas() 
RETURNS TRIGGER AS $tarifasNulas$
  BEGIN
    IF EXISTS (select * from PLAN_PREPAGO where codplan=NEW.codplan) THEN
      IF NEW.tarifa IS NULL THEN RETURN NULL;
      ELSE RETURN NEW;
      END IF;
    END IF;
  END;  
$tarifasNulas$ LANGUAGE plpgsql;

CREATE TRIGGER tarifasNulas
BEFORE INSERT ON INCLUYE FOR EACH ROW 
EXECUTE PROCEDURE tarifasNulas();
