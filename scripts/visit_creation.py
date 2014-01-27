import os, sys

path='/home/sheefrex/code/cattalax/site' # ntc
if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]="cattalax.settings"

from django.core.management import setup_environ
from cattalax import settings
from dashboard.models import Customer, Outlet, Visit

setup_environ(settings)

#import MySQLdb
from duration import *

# DJANGO_SETTINGS_MODULE = cattalax.settings
#settings.configure(
#	DATABASE_ENGINE='mysql',
#	DATABASE_NAME='cat_dashboard',
#	DATABASE_USER='root',
#	DATABASE_PASSWORD='the power to do what is right',
#	DATABASE_HOST='localhost',
#	)
# HOST="localhost"
# USER="root"
# PW="the power to do what is right"
# DB="cattalax"

# con = MySQLdb.connect(HOST,USER,PW,DB)
# cur = con.cursor()

# cur.execute("SELECT id FROM enters WHERE obs>2 INTO OUTFILE '/tmp/enter2.csv' fields terminated by ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'")

file_of_addrs = open("/tmp/enter2.csv")
addrs = file_of_addrs.read().split()

count0 = 0
for addr in addrs:
	if len(Customer.objects.filter(mac_addr=eval(addr)))==0:
		c = Customer(mac_addr=eval(addr))
		c.save()
	count0 += 1
	filename = '/tmp/detail' + str(count0) + '.csv'
#	sql_command = "SELECT DISTINCT * FROM attendance WHERE id="+addr+" ORDER BY timestamp, -rssi INTO OUTFILE '"+filename+"' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'"
#	print sql_command
#	cur.execute(sql_command)
	print "Getting duration, and inserting to customer_log table."
	g_d = robjects.r('get_duration(\"' + filename + '\")')
	visits = len(g_d)/4
	count = 0
	for i in range(visits):
#		cur.execute("INSERT INTO customer_log(Id, arrival_time, duration, leave_time, instantiated) VALUES('%s', %d, %d, %d, %d)" % (g_d[count], int(g_d[count+1]), int(g_d[count+2]), int(g_d[count+3]), 0))
		customer = Customer.objects.get(mac_addr=g_d[count])
		outlet = Outlet.objects.get(sensor_no=1)
		v = Visit(patron=customer, vendor=outlet, arrival_time=int(g_d[count+1]), duration=int(g_d[count+2]))
		print v.patron
		print v.vendor
		print v.arrival_time
		print v.duration
		v.save()
		count += 4

#	con.commit()
# 	os.remove('tmp/cattalax/enter2.csv')	
