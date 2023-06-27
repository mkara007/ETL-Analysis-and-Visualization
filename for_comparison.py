import yaml
import mysql.connector as sql
import matplotlib.pyplot as plt
import pandas as pd

# Connecting to the MySQL database
db = yaml.safe_load(open('db.yaml'))
config = {
    'user':     db['user'],
    'password': db['pwrd'],
    'host':     db['host'],
    'database': db['db'],
    'auth_plugin': 'mysql_native_password'
}

cnx = sql.connect(**config)

cursor = cnx.cursor()

query_building = ("""
SELECT 
    period, 
    CAST(SUM(Sales) AS UNSIGNED) AS building_sales
FROM final_data
WHERE 
    `Kind of Business` LIKE 'Building mat. and supplies dealers'
GROUP BY 1;
""")
building = pd.read_sql_query(query_building, cnx)

query_paint = ("""
SELECT 
    period, 
    CAST(SUM(Sales) AS UNSIGNED) AS paint_sales
FROM final_data
WHERE 
    `Kind of Business` LIKE 'Paint and wallpaper stores'
GROUP BY 1;
""")
paint = pd.read_sql_query(query_paint, cnx)

query_hardware = ("""
SELECT 
    period, 
    CAST(SUM(Sales) AS UNSIGNED) AS hardware_sales
FROM final_data
WHERE 
    `Kind of Business` LIKE 'Hardware stores'
GROUP BY 1;
""")
hardware = pd.read_sql_query(query_hardware, cnx)

for_comparison = building.copy()
for_comparison = for_comparison.merge(paint, how = 'left', on = 'period')
for_comparison = for_comparison.merge(hardware, how = 'left', on = 'period')

for_comparison.to_csv('for_comparison.csv')

cursor.close()
cnx.close()