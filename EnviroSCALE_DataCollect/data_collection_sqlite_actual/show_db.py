import sqlite3
import DEFINE
from xlsxwriter.workbook import Workbook
workbook = Workbook(str(DEFINE.DB_NAME)+".xlsx")
worksheet = workbook.add_worksheet()
sqlite_file = str(DEFINE.DB_NAME)+".sqlite"

worksheet.write('A1', 'ID')
worksheet.write('B1', 'Timestamp')
worksheet.write('C1', 'CH4')
worksheet.write('D1', 'LPG')
worksheet.write('E1', 'CO2')
worksheet.write('F1', 'Dust')
worksheet.write('G1', 'Temperature')
worksheet.write('H1', 'Humidity')
worksheet.write('I1', 'Lat')
worksheet.write('J1', 'Long')

conn=sqlite3.connect(sqlite_file)
c=conn.cursor()
mysel=c.execute("select * from sensors_values ")
for i, row in enumerate(mysel):
    for j, value in enumerate(row):
        worksheet.write(i+1, j, value)
workbook.close()

