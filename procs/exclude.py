import os, sys
import MySQLdb


HOST="localhost"
USER="root"
PW="the power to do what is right"
DB="cattalax"
con = MySQLdb.connect(HOST,USER,PW,DB)
cur = con.cursor()

file_of_addrs = open("/root/exclude.csv")
addrs = file_of_addrs.read().split(',')

for addr in addrs:
	stmt = "DELETE FROM `attendance` WHERE id='BSSID:ff:ff:ff:ff:ff:ff' AND sensor_id=13"  
	print stmt
	cur.execute(stmt)
	con.commit()





