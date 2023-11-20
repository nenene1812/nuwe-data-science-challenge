# discover from dataset

## This is some insight from the dataset already discovered.

# Insight from Green Energy Gen dataset 

1. 2021-12-31 only have 2021-12-31T23:45+00:00Z	2022-01-01T00:00+00:00Z -> Action: Delete this date 
2. Check Null value 
```
StartTime    0
EndTime      0
UnitName     0
PsrType      0
quantity     0
Country      0
dtype: int64
```
3. 412406 have quantity equal = 0 -> 1/3 dataset 
4. total records 9 countries: 1466395
5. 1 hour include 4 timeframe
example 
```
2022-01-01T00:00+00:00Z	2022-01-01T00:15+00:00Z	
2022-01-01T00:15+00:00Z	2022-01-01T00:30+00:00Z
2022-01-01T00:30+00:00Z	2022-01-01T00:45+00:00Z
2022-01-01T00:45+00:00Z	2022-01-01T01:00+00:00Z
``` 
-> For hourly prediction, the strategy is to combine four recordings into one. DataHour is taken from StartTime as the root hour for the new record based on the nature of the data.

# Insight from Green Energy Load dataset 

-> The same like green Energy gen dataset => Insight also the same. 

# Insight from consolidate dataset 

1. Check NaN 
```
	index	nan_count
0	StartDate	0
1	dataHour	0
2	green_energy_HU	0
3	green_energy_IT	0
4	green_energy_PO	0
5	green_energy_SP	0
6	green_energy_UK	0
7	green_energy_DE	0
8	green_energy_DK	0
9	green_energy_SE	0
10	green_energy_NE	0
11	load_HU	0
12	load_IT	0
13	load_PO	0
14	load_SP	0
15	load_UK	0
16	load_DE	0
17	load_DK	0
18	load_SE	0
19	load_NE	0
20	index	0
```