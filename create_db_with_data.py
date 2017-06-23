import csv
import sqlite3
from datetime import date
from datetime import time

conn = sqlite3.connect("viccrashes.sqlite3")
conn.text_factory = str
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS crashes_last_five_years")

sql = """
    CREATE TABLE `crashes_last_five_years` (
	`X`	REAL,
	`Y`	REAL,
	`OBJECTID`	INTEGER PRIMARY KEY,
	`ACCIDENT_NO`	TEXT,
	`ABS_CODE`	TEXT,
	`ACCIDENT_STATUS`	TEXT,
	`ACCIDENT_DATE`	TEXT,
	`ACCIDENT_TIME`	TEXT,
	`ALCOHOLTIME`	TEXT,
	`ACCIDENT_TYPE`	TEXT,
	`DAY_OF_WEEK`	TEXT,
	`DCA_CODE`	TEXT,
	`HIT_RUN_FLAG`	TEXT,
	`LIGHT_CONDITION`	TEXT,
	`POLICE_ATTEND`	TEXT,
	`ROAD_GEOMETRY`	TEXT,
	`SEVERITY`	TEXT,
	`SPEED_ZONE`	TEXT,
	`RUN_OFFROAD`	TEXT,
	`NODE_ID`	INTEGER,
	`LONGITUDE`	REAL,
	`LATITUDE`	REAL,
	`NODE_TYPE`	TEXT,
	`LGA_NAME`	TEXT,
	`REGION_NAME`	TEXT,
	`VICGRID_X`	REAL,
	`VICGRID_Y`	REAL,
	`TOTAL_PERSONS`	INTEGER,
	`INJ_OR_FATAL`	INTEGER,
	`FATALITY`	INTEGER,
	`SERIOUSINJURY`	INTEGER,
	`OTHERINJURY`	INTEGER,
	`NONINJURED`	INTEGER,
	`MALES`	INTEGER,
	`FEMALES`	INTEGER,
	`BICYCLIST`	INTEGER,
	`PASSENGER`	INTEGER,
	`DRIVER`	INTEGER,
	`PEDESTRIAN`	INTEGER,
	`PILLION`	INTEGER,
	`MOTORIST`	INTEGER,
	`UNKNOWN`	INTEGER,
	`PED_CYCLIST_5_12`	INTEGER,
	`PED_CYCLIST_13_18`	INTEGER,
	`OLD_PEDESTRIAN`	INTEGER,
	`OLD_DRIVER`	INTEGER,
	`YOUNG_DRIVER`	INTEGER,
	`ALCOHOL_RELATED`	TEXT,
	`UNLICENCSED`	INTEGER,
	`NO_OF_VEHICLES`	INTEGER,
	`HEAVYVEHICLE`	INTEGER,
	`PASSENGERVEHICLE`	INTEGER,
	`MOTORCYCLE`	INTEGER,
	`PUBLICVEHICLE`	INTEGER,
	`DEG_URBAN_NAME`	TEXT,
	`DEG_URBAN_ALL`	TEXT,
	`LGA_NAME_ALL`	TEXT,
	`REGION_NAME_ALL`	TEXT,
	`SRNS`	TEXT,
	`SRNS_ALL`	TEXT,
	`RMA`	TEXT,
	`RMA_ALL`	TEXT,
	`DIVIDED`	TEXT,
	`DIVIDED_ALL`	TEXT,
	`STAT_DIV_NAME`	TEXT,
    `ACCIDENT_DATETIME` TEXT
);
"""

c.execute(sql)

with open("Crashes_Last_Five_Years.csv") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for idx, row in enumerate(csvreader):
        if idx == 0:
			continue
        dateparts = row[6].split("/")
        d = date(int(dateparts[2]), int(dateparts[1]), int(dateparts[0]))
        row[6] = d.isoformat()

        timeparts = row[7].split(".")
        t = time(int(timeparts[0]), int(timeparts[1]), int(timeparts[2]))
        row[7] = t.isoformat()

        dt = row[6] + ' ' + row[7]
        row.append(dt)
        c.execute("INSERT INTO crashes_last_five_years VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row)

conn.commit()
conn.close()

