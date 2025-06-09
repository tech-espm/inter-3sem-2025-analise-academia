CREATE DATABASE IF NOT EXISTS academia DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;

-- Todos os deltas estão em segundos

USE academia;

-- Cada uma das 8 zonas (0 ... 7) será mapeada como um id_sensor (1 ... 8)
-- topic espm/stainel/hpd/DetectedPersonsZone
-- {"DetectedPersonsZone":[0,0,2,1,1,0,1,0]}
-- topic espm/stainel/hpd/LuxZone
-- {"LuxZone":[70.00,78.00,74.00,87.00,67.00,57.00,50.00,53.00]}
-- topic espm/stainel/hpd/Humidity
-- {"Humidity":67.00}
-- topic espm/stainel/hpd/Temperature
-- {"Temperature":24.30}
CREATE TABLE pca (
  id bigint NOT NULL,
  data datetime NOT NULL,
  id_sensor tinyint NOT NULL,
  delta int NOT NULL, -- O campo delta diz respeito a alterações no valor de pessoas
  pessoas tinyint NOT NULL,
  luminosidade float NOT NULL,
  umidade float NOT NULL,
  temperatura float NOT NULL,
  PRIMARY KEY (id),
  KEY pca_data_id_sensor (data, id_sensor),
  KEY pca_id_sensor (id_sensor)
);

-- topic v3/espm/devices/passage01/up
-- topic v3/espm/devices/passage02/up
-- { "end_device_ids": { "device_id": "passage01" }, "uplink_message": { "rx_metadata": [{ "timestamp": 2040934975 }], "decoded_payload": { "battery": 0, "period_in": 0, "period_out": 0 } } }
CREATE TABLE passagem (
  id bigint NOT NULL,
  data datetime NOT NULL,
  id_sensor tinyint NOT NULL,
  delta int NOT NULL,
  bateria tinyint NOT NULL,
  entrada int NOT NULL,
  saida int NOT NULL,
  PRIMARY KEY (id),
  KEY passagem_data_id_sensor (data, id_sensor),
  KEY passagem_id_sensor (id_sensor)
);

-- Query de monitoramento em tempo real de presença por zona
(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 1 order by id desc limit 1)
union all
(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 2 order by id desc limit 1)
union all
(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 3 order by id desc limit 1)
union all
(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 4 order by id desc limit 1)
union all
(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 5 order by id desc limit 1)
union all
(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 6 order by id desc limit 1)
union all
(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 7 order by id desc limit 1)
union all
(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 8 order by id desc limit 1)
;

-- Query de consolidação de ocupação máxima por zona por dia do mês e por hora, para o heatmap de visão explodida por dia do mês com N colunas e 24 linhas
-- Para preencher os dias/horas faltantes:
-- Se o primeiro registro do dia não for às 00:00 preencher com 0 todas as horas das 00:00 até a primeira retornada
-- Os registros faltantes ao longo do dia devem ser preenchidos com o valor do campo ultimo_pessoas do último registro retornado
select tmp.id_sensor, tmp.dia, tmp.hora, tmp.pessoas, u.pessoas ultimo_pessoas from
(
	select id_sensor, date_format(date(data), '%d/%m/%Y') dia, extract(hour from data) hora, max(pessoas) pessoas, max(id) id_ultimo
	from pca
	where data between '2025-03-03 00:00:00' and '2025-03-14 23:59:59'
	group by id_sensor, dia, hora
	order by id_sensor, dia, hora
) tmp
inner join pca u on u.id = tmp.id_ultimo;

-- Query de consolidação por dia do mês e por hora, para o heatmap de visão explodida por dia do mês com N colunas e 24 linhas
select date_format(date(data), '%d/%m/%Y') dia, extract(hour from data) hora, sum(entrada) entrada
from passagem
where data between '2025-03-03 00:00:00' and '2025-03-14 23:59:59'
and id_sensor = 2
group by dia, hora;

-- Query de consolidação por dia do mês, para o heatmap de visão explodida por dia do mês com N colunas e 24 linhas
select date_format(date(data), '%d/%m/%Y') dia, sum(entrada) entrada
from passagem
where data between '2025-03-03 00:00:00' and '2025-03-14 23:59:59'
and id_sensor = 2
group by dia;


-- Média do pico de pessoas por hora no período 

select avg(tmp.pessoas), tmp.hora
from (select max(pessoas) as pessoas, date_format(date(data), '%Y/%m/%d') dia, extract(hour from data) hora
  from pca
  where data between '2025-03-03 00:00:00' and '2025-03-14 23:59:59'
  group by dia,hora) tmp
  group by hora
  order by hora;

-- Média de pessoas por zona no período

  select id_sensor, avg(pessoas)
	from pca
    where extract(hour from data) > 6 and data between '2025-03-03 00:00:00' and '2025-03-14 23:59:59'
    group by id_sensor;