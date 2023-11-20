-- Select_all_energy_data_gen
with data_raw as (
  SELECT
  substr(StartTime, 1, 10) as StartDate,
  substr(EndTime, 1, 10) as EndDate,
  substr(StartTime, 12, 2) as dataHour,
  *
FROM energy_data_gen
)

SELECT * FROM data_raw;

-- Transform_load_data
with data_raw as (
  SELECT
  substr(StartTime, 1, 10) as StartDate,
  substr(EndTime, 1, 10) as EndDate,
  substr(StartTime, 12, 2) as dataHour,
  *
FROM energy_data_load
WHERE StartDate <> '2021-12-31')

  SELECT StartDate,EndDate,dataHour,
  SUM(CASE WHEN Country = 'HU' THEN Load ELSE 0 END) AS load_HU,
  SUM(CASE WHEN Country = 'IT' THEN Load ELSE 0 END) AS load_IT,
  SUM(CASE WHEN Country = 'PO' THEN Load ELSE 0 END) AS load_PO,
  SUM(CASE WHEN Country = 'SP' THEN Load ELSE 0 END) AS load_SP,
  SUM(CASE WHEN Country = 'UK' THEN Load ELSE 0 END) AS load_UK,
  SUM(CASE WHEN Country = 'DE' THEN Load ELSE 0 END) AS load_DE,
  SUM(CASE WHEN Country = 'DK' THEN Load ELSE 0 END) AS load_DK,
  SUM(CASE WHEN Country = 'SE' THEN Load ELSE 0 END) AS load_SE,
  SUM(CASE WHEN Country = 'NE' THEN Load ELSE 0 END) AS load_NE
FROM  data_raw
GROUP BY 1,2,3; 

-- Transform_join_load_gen

with data_raw_load as (
SELECT
  substr(StartTime, 1, 10) as StartDate,
  substr(EndTime, 1, 10) as EndDate,
  substr(StartTime, 12, 2) as dataHour,
  *
FROM energy_data_load
WHERE StartDate <> '2021-12-31'),

data_raw_gen as (
SELECT
  substr(StartTime, 1, 10) as StartDate,
  substr(EndTime, 1, 10) as EndDate,
  substr(StartTime, 12, 2) as dataHour,
  *
FROM energy_data_gen
WHERE StartDate <> '2021-12-31'),

agg_data_load as (
SELECT StartDate,dataHour,
  SUM(CASE WHEN Country = 'HU' THEN Load ELSE 0 END) AS load_HU,
  SUM(CASE WHEN Country = 'IT' THEN Load ELSE 0 END) AS load_IT,
  SUM(CASE WHEN Country = 'PO' THEN Load ELSE 0 END) AS load_PO,
  SUM(CASE WHEN Country = 'SP' THEN Load ELSE 0 END) AS load_SP,
  SUM(CASE WHEN Country = 'UK' THEN Load ELSE 0 END) AS load_UK,
  SUM(CASE WHEN Country = 'DE' THEN Load ELSE 0 END) AS load_DE,
  SUM(CASE WHEN Country = 'DK' THEN Load ELSE 0 END) AS load_DK,
  SUM(CASE WHEN Country = 'SE' THEN Load ELSE 0 END) AS load_SE,
  SUM(CASE WHEN Country = 'NE' THEN Load ELSE 0 END) AS load_NE
FROM  data_raw_load
GROUP BY 1,2
order by 1,2), 

agg_data_gen as (
SELECT StartDate,dataHour,
  SUM(CASE WHEN Country = 'HU' THEN quantity ELSE 0 END) AS green_energy_HU,
  SUM(CASE WHEN Country = 'IT' THEN quantity ELSE 0 END) AS green_energy_IT,
  SUM(CASE WHEN Country = 'PO' THEN quantity ELSE 0 END) AS green_energy_PO,
  SUM(CASE WHEN Country = 'SP' THEN quantity ELSE 0 END) AS green_energy_SP,
  SUM(CASE WHEN Country = 'UK' THEN quantity ELSE 0 END) AS green_energy_UK,
  SUM(CASE WHEN Country = 'DE' THEN quantity ELSE 0 END) AS green_energy_DE,
  SUM(CASE WHEN Country = 'DK' THEN quantity ELSE 0 END) AS green_energy_DK,
  SUM(CASE WHEN Country = 'SE' THEN quantity ELSE 0 END) AS green_energy_SE,
  SUM(CASE WHEN Country = 'NE' THEN quantity ELSE 0 END) AS green_energy_NE
FROM  data_raw_gen
GROUP BY 1,2
order by 1,2
)
SELECT a.*,b.load_HU,b.load_IT,b.load_PO,b.load_SP,b.load_UK,b.load_DE,load_DK,b.load_SE,load_NE
FROM agg_data_gen as a 
LEFT JOIN  agg_data_load as b using(StartDate,dataHour);