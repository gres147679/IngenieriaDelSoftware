/*
Trigger que se encarga de la primera restricción explícita:
1. Un producto debe estar asociado a un plan prepago o a un plan postpago y no  a
ambos.
*/
CREATE OR REPLACE FUNCTION existePlanPrepago()
RETURNS TRIGGER AS $existePlanPrepago$  
  BEGIN

    IF EXISTS (SELECT * 
              FROM ACTIVA AS origen
              WHERE NEW.numserie = origen.numserie) THEN RETURN NULL;
    END IF;
    RETURN NEW;
    
  END;
$existePlanPrepago$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION existePlanPostpago()
RETURNS TRIGGER AS $existePlanPostpago$
  BEGIN

    IF EXISTS (SELECT * 
              FROM AFILIA AS origen
              WHERE NEW.numserie = origen.numserie) THEN RETURN NULL;
    END IF;
    RETURN NEW;
  END;
$existePlanPostpago$ LANGUAGE plpgsql;
  
CREATE TRIGGER existePlanPrepago
BEFORE INSERT OR UPDATE ON ACTIVA FOR EACH ROW 
EXECUTE PROCEDURE existePlanPostpago();
  
CREATE TRIGGER existePlanPostpago 
BEFORE INSERT OR UPDATE ON AFILIA FOR EACH ROW 
EXECUTE PROCEDURE existePlanPrepago();


/*
Trigger que se encarga de la segunda restricción explícita:
2. Si un servicio es único, el atributo cantidad en cada instancia de las
interrelaciones consume, contiene e incluye debe valer 1
*/
CREATE OR REPLACE FUNCTION servicioEsUnico() 
RETURNS TRIGGER AS $servicioEsUnico$
DECLARE esunico boolean;
  BEGIN
    SELECT INTO esunico unico 
    FROM SERVICIO AS origen 
    WHERE origen.codserv=NEW.codserv);
    IF esunico THEN
      IF NEW.cantidad = 1 AND NOT EXISTS(select * from CONSUME AS 
      origen where origen.numSerie = NEW.numSerie AND origen.codserv = NEW.codserv)
      THEN RETURN NEW;
      ELSE RETURN NULL;
      END IF;
    END IF;
  END;
$servicioEsUnico$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION servicioEsUnico2() 
RETURNS TRIGGER AS $servicioEsUnico2$
DECLARE esunico boolean;
  BEGIN
    SELECT INTO esunico unico 
    FROM SERVICIO AS origen 
    WHERE origen.codserv=NEW.codserv);
    IF esunico THEN
      IF NEW.cantidad = 1 AND NOT EXISTS(select * from INCLUYE AS 
      origen where origen.numSerie = NEW.numSerie AND origen.codserv = NEW.codserv)
      THEN RETURN NEW;
      ELSE RETURN NULL;
      END IF;
    END IF;
  END;
$servicioEsUnico2$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION servicioEsUnico3() 
RETURNS TRIGGER AS $servicioEsUnico3$
DECLARE esunico boolean;
  BEGIN
    SELECT INTO esunico unico 
    FROM SERVICIO AS origen 
    WHERE origen.codserv=NEW.codserv);
    IF esunico THEN
      IF NEW.cantidad = 1 AND NOT EXISTS(select * from CONTIENE AS 
      origen where origen.numSerie = NEW.numSerie AND origen.codserv = NEW.codserv)
      THEN RETURN NEW;
      ELSE RETURN NULL;
      END IF;
    END IF;
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


-- /*
-- Trigger que se encarga de la tercera restricción explícita:
-- 3. Si un paquete aparece sólo una vez en la interrelación contiene,
-- entonces el costo del paquete es el mismo costo del servicio que contiene.
-- */
-- CREATE OR REPLACE FUNCTION costoPaquete() 
-- RETURNS TRIGGER AS $costoPaquete$
-- 
-- BEGIN
--     IF (SELECT count(*)
--         FROM CONTIENE AS origen 
--         WHERE origen.codpaq=NEW.codpaq)=0 THEN
--       
--       IF (SELECT precio 
--           FROM paquete AS origen
--           WHERE origen.codpaq = NEW.codpaq) =
--         
--          (SELECT costo 
--           FROM servicio AS origen 
--           WHERE origen.codserv = NEW.codserv) THEN RETURN NEW;
--       ELSE RETURN NULL;
--       END IF;
--     
--     END IF;
-- END;
-- $costoPaquete$ LANGUAGE plpgsql;
--   
-- CREATE TRIGGER costoPaquete 
-- BEFORE INSERT ON CONTIENE FOR EACH ROW 
-- EXECUTE PROCEDURE costoPaquete();




-- -- Trigger que se encarga de la cuarta restricción explícita y la quinta
-- -- 4. Un producto no puede consumir ningún servicio (aparecer en la
-- -- interrelación
-- -- consume) si no está afiliado algún plan postpago o prepago (ver restricción
-- -- 5. Un producto no puede consumir ningún servicio en una fecha (aparecer en la
-- -- interrelación consume) si no está afiliado algún plan prepago con saldo
-- -- positivo
-- -- en esa misma fecha
-- 
-- CREATE OR REPLACE FUNCTION productoAfiliado() 
-- RETURNS TRIGGER AS $productoAfiliado$
-- DECLARE 
-- saldo_actual real;
-- cobro real;
-- 
-- BEGIN
-- IF EXISTS (SELECT * 
-- FROM AFILIA AS post
-- WHERE NEW.numserie = post.numserie) THEN RETURN NEW;
-- END IF;
-- 
-- IF EXISTS (SELECT INTO saldo_actual saldo 
-- FROM ACTIVA AS pre
-- WHERE NEW.numserie = pre.numserie) THEN
-- 
-- SELECT INTO cobro tarifa
-- FROM PRODUCTO NATURAL JOIN ACTIVA NATURAL JOIN INCLUYE
-- WHERE numserie = NEW.numserie;
-- 
-- IF (saldo_actual - cobro < 0) THEN RETURN NULL;
-- ELSE RETURN NEW;
-- END IF;
-- 
-- END IF;
-- 
-- RETURN NULL;
--   END;
-- $productoAfiliado$ LANGUAGE plpgsql;




-- -- Trigger que se encarga de la sexta restricción explícita
-- -- 6. Un plan que incluye un servicio debe tener una cantidad no nula y una
-- -- tarifa nula si es postpago. Debe tener una cantidad nula y una tarifa no nula
-- -- si
-- -- es prepago.
-- 
-- CREATE OR REPLACE FUNCTION inclusionServicio() 
-- RETURNS TRIGGER AS $inclusionServicio$
-- 
-- BEGIN
-- 
-- --     Si es prepago
-- IF EXISTS (SELECT *
-- FROM PLAN_PREPAGO p
-- WHERE p.codplan = new.codplan) THEN
-- 
-- IF (new.tarifa <> NULL) AND (new.cantidad = NULL) THEN RETURN NEW;
-- ELSE RETURN NULL;
-- END IF;
-- 
-- END IF;
-- 
-- IF EXISTS (SELECT *
-- FROM PLAN_POSTPAGO p
-- WHERE p.codplan = new.codplan) THEN
-- 
-- IF (new.tarifa = NULL) AND (new.cantidad <> NULL) THEN RETURN NEW;
-- ELSE RETURN NULL;
-- END IF;
-- 
-- END IF;
-- END;
-- $inclusionServicio$ LANGUAGE plpgsql;
-- 
-- CREATE TRIGGER inclusionServicio
-- BEFORE INSERT OR UPDATE ON INCLUYE FOR EACH ROW 
-- EXECUTE PROCEDURE inclusionServicio();