-- Crear tabla tipo_tarifa y cargar del archivo tipos_tarifa.csv
CREATE TABLE tipo_tarifa (
    codigo INT,
    tarifa VARCHAR(20)
);
COPY "taxi-test".public.tipo_tarifa (codigo, tarifa) FROM 's3://bigdata-henry-52024/utils/tipos_tarifa.csv' IAM_ROLE 'arn:aws:iam::<IAM>:role<ROL>' FORMAT AS CSV DELIMITER ',' QUOTE '"' IGNOREHEADER 1 REGION AS 'us-east-1'

-- Crear tabla tipo_tarifa y cargar del archivo tipos_pago.csv
CREATE TABLE tipo_pago (
    codigo INT,
    pago VARCHAR(20)
);
COPY "taxi-test".public.tipo_pago (codigo, tarifa) FROM 's3://bigdata-henry-52024/utils/tipos_pago.csv' IAM_ROLE 'arn:aws:iam::<IAM>:role<ROL>' FORMAT AS CSV DELIMITER ',' QUOTE '"' IGNOREHEADER 1 REGION AS 'us-east-1'

-- Crear tabla zona_taxi
CREATE TABLE zona_taxi (
    idzona INT,
    barrio VARCHAR(20),
    zona VARCHAR(100),
);

-- Crear tabla temporal zona_taxi2 y cargar del archivo taxi_zones_lookup.csv
-- Dado que el formato del archivo no coincide con los datos que se guardarán, se cargarán en la tabla temporal, se procesarán y se guardarán en la tabla permanente
CREATE TEMPORARY TABLE zona_taxi2 (
    idzona INT,
    barrio VARCHAR(20),
    zona VARCHAR(100),
    zona_servicio VARCHAR(20)
);
COPY "taxi-test".public.zona_taxi2 FROM 's3://bigdata-henry-52024/utils/taxi_zone_lookup.csv' IAM_ROLE 'arn:aws:iam::<ROL>:role<ROL>' FORMAT AS CSV DELIMITER ',' QUOTE '"' IGNOREHEADER 1 REGION AS 'us-east-1'

-- Limpiar y cargar en la tabla zona_taxi
UPDATE zona_taxi2 SET barrio = 'Unknown'
WHERE barrio = 'N/A';

INSERT INTO "taxi-test".public.zona_taxi
(SELECT idzona, barrio, zona FROM zona_taxi2);

-- Crear tabla viaje_taxi
CREATE TABLE "taxi-test".public.viaje_taxi (
    tipo_vehiculo VARCHAR(20),
    hora_abordaje TIMESTAMP,
    duracion FLOAT8,
    conteo_pasajeros BIGINT,
    distancia_recorrida FLOAT8,
    tipo_tarifa BIGINT,
    tipo_pago BIGINT,
    localizacion_abordaje INT,
    localizacion_destino INT,
    total FLOAT8
);

-- Crear tabla temporal  viaje_taxi2
-- Dado que el formato de los archivos no coincide con los datos que se guardarán, se cargarán en la tabla temporal, se procesarán y se guardarán en la tabla permanente
CREATE TEMPORARY TABLE viaje_taxi2(
    vendorid FLOAT8,
    hora_abordaje TIMESTAMP,
    hora_bajada TIMESTAMP,
    store_and_fwd VARCHAR(5),
    tipo_tarifa FLOAT8,
    localizacion_abordaje BIGINT,
    localizacion_destino BIGINT,
    conteo_pasajeros FLOAT8,
    distancia_recorrida FLOAT8,
    monto_base FLOAT8,
    extra FLOAT8,
    mta_tax FLOAT8,
    propina FLOAT8,
    peajes FLOAT8,
    ehail FLOAT8,
    recargo_mejora FLOAT8,
    total FLOAT8,
    tipo_pago FLOAT8,
    recargo_congestion FLOAT8
);

-- Algunos campos tienen formatos diferentes entre varios archivos
ALTER TABLE viaje_taxi2
ALTER COLUMN vendorid TYPE FLOAT8, conteo_pasajeros TYPE BIGINT, tipo_tarifa TYPE BIGINT, tipo_pago TYPE BIGINT;

-- Los archivos de taxis verdes tienen un campo adicional trip_type, que indica si el viaje fue asignado o recogido en la vía
ALTER TABLE viaje_taxi2
ADD COLUMN tipo_viaje INT;

/* Dado que los diferentes formatos requerían realizar cambios en la estructura de la tabla temporal,
se ejecutaron las siguientes sentencias según se cargaban archivos, se cargaban en la tabla permanente,
luego se modificaba la tabla temporal, y se realizaba nuevamente el proceso.*/

-- Cargar archivos de taxis amarillos en la tabla permanente
-- El comando COPY añade los registros encontrados
-- Cambiar el año entre 2022 y 2023 y el mes entre 01 y 12
COPY viaje_taxi2 FROM 's3://bigdata-henry-52024/nyc-yellow-taxis/yellow_tripdata_2022-01.parquet' IAM_ROLE 'arn:aws:iam::<IAM>:role<ROL>' FORMAT AS PARQUET;

-- Cargar archivos de taxis verdes en la tabla permanente
-- Cambiar el año entre 2022 y 2023 y el mes entre 01 y 12
COPY viaje_taxi2 FROM 's3://bigdata-henry-52024/nyc-green-taxis/green_tripdata_2022-01.parquet' IAM_ROLE 'arn:aws:iam::<IAM>:role<ROL>' FORMAT AS PARQUET;

-- Eliminar registros con más de 6 pasajeros
DELETE FROM viaje_taxi2
WHERE conteo_pasajeros > 6;

-- Para comprobar y eliminar los duplicados se creó otra tabla auxiliar con una consulta distinct
CREATE TEMPORARY TABLE viajes AS
SELECT DISTINCT vendorid, hora_abordaje, hora_bajada, store_and_fwd, tipo_tarifa,
    localizacion_abordaje, localizacion_destino, conteo_pasajeros, distancia_recorrida, monto_base,
    extra, mta_tax, propina, peajes, ehail, recargo_mejora, total, tipo_pago, recargo_congestion
FROM viaje_taxi;

DELETE FROM viaje_taxi2;

INSERT INTO viaje_taxi2
SELECT * FROM viajes;

-- Agregar columna duración para almacenar la duración del viaje
ALTER TABLE viaje_taxi2 ADD COLUMN duracion FLOAT8;

-- Crear función para calcular la duración del viaje en minutos
CREATE OR REPLACE FUNCTION get_duracion_viaje
(TIMESTAMP, TIMESTAMP)
RETURNS FLOAT8 STABLE AS $$
    SELECT EXTRACT(minute FROM ($2-$1))
$$ language sql;

-- Guardar la duración de los viajes
UPDATE viaje_taxi2 SET duracion = get_duracion_viaje(hora_abordaje, hora_bajada);

-- Se corrigieron los registros donde el total estaba negativo
UPDATE viaje_taxi2
SET total = ABS(total) WHERE total < 0;

-- Se corrigieron los registros donde el conteo de pasajeros estaba como nulo
UPDATE viaje_taxi2
SET conteo_pasajeros=1 WHERE conteo_pasajeros is NULL;

/* Para insertar los datos en la tabla permanente se comprobaron las siguientes condiciones:
   - Que la duración en minutos fuera menor o igual a 2 horas
   - Que la distancia recorrida en millas fuera menor o igual a 50
   - Que los registros dataran desde el 01-01-2022 en adelante

   Además, algunas columnas se conviertieron a los tipos adecuados según el caso
*/
-- Insertar registrs de taxis amarillos
INSERT INTO "taxi-test".public.viaje_taxi (tipo_vehiculo, hora_abordaje, duracion, conteo_pasajeros, distancia_recorrida, tipo_tarifa, tipo_pago, localizacion_abordaje, localizacion_destino, total) (
SELECT 'yellow', hora_abordaje, duracion, CAST(ROUND(conteo_pasajeros) AS BIGINT), distancia_recorrida, CAST(ROUND(tipo_tarifa) AS BIGINT), tipo_pago, CONVERT(INT, localizacion_abordaje), CONVERT(INT, localizacion_destino), total
FROM viaje_taxi2
WHERE duracion <= 180 AND distancia_recorrida <= 50 AND total <= 200 AND hora_abordaje >= TO_TIMESTAMP('2022-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
);

-- Insertar registros de taxis verdes
-- En este caso, se indicó si correspondía a un viaje acordado en la vía (streethail) o asignado (dispatch)
INSERT INTO "taxi-test".public.viaje_taxi (tipo_vehiculo, hora_abordaje, duracion, conteo_pasajeros, distancia_recorrida, tipo_tarifa, tipo_pago, localizacion_abordaje, localizacion_destino, total) (
SELECT 'green-streethail', hora_abordaje, duracion, CAST(ROUND(conteo_pasajeros) AS BIGINT), distancia_recorrida, CAST(ROUND(tipo_tarifa) AS BIGINT), tipo_pago, CONVERT(INT, localizacion_abordaje), CONVERT(INT, localizacion_destino), total
FROM viaje_taxi2
WHERE duracion <= 180 AND distancia_recorrida <= 50 AND total <= 200 AND hora_abordaje >= TO_TIMESTAMP('2022-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS') AND tipo_viaje = 1
);

INSERT INTO "taxi-test".public.viaje_taxi (tipo_vehiculo, hora_abordaje, duracion, conteo_pasajeros, distancia_recorrida, tipo_tarifa, tipo_pago, localizacion_abordaje, localizacion_destino, total) (
SELECT 'green-dispatch', hora_abordaje, duracion, CAST(ROUND(conteo_pasajeros) AS BIGINT), distancia_recorrida, CAST(ROUND(tipo_tarifa) AS BIGINT), tipo_pago, CONVERT(INT, localizacion_abordaje), CONVERT(INT, localizacion_destino), total
FROM viaje_taxi2
WHERE duracion <= 180 AND distancia_recorrida <= 50 AND total <= 200 AND hora_abordaje >= TO_TIMESTAMP('2022-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS') AND tipo_viaje = 1
);