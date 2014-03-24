import os, sys
import MySQLdb
import calendar
from datetime import datetime, date
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import datetime as datetime2
from duration import *
import pytz

# Connect to web database
path='/root/.virtualenvs/cattalax/cattalax' 
if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]="cattalax.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cattalax.settings")

from dashboard.models import *
# Connect to hoover database
HOST="localhost"
USER="root"
PW="the power to do what is right"
DB="cattalax"
con = MySQLdb.connect(HOST,USER,PW,DB)
cur = con.cursor()


shop_list = [shop.sensor_no for shop in Outlet.objects.all()]

dt = date.today()
start_dt = datetime(dt.year, dt.month, dt.day-7)
start_timestamp = calendar.timegm(start_dt.utctimetuple())

def calculate_view(shop_no, start_time, cursor):
	view_name = "capture"+str(shop_no)
	cursor.execute("CREATE OR REPLACE VIEW "+view_name+" AS SELECT DISTINCT id, timestamp, count(id) AS obs FROM attendance WHERE sensor_id="+str(shop_no)+" AND timestamp>"+str(start_time)+" GROUP BY id")
	return view_name

def captures_in_shop(shop_no, cursor):
	view = calculate_view(shop_no, start_timestamp, cursor)
	stmt = "SELECT id FROM "+view+" WHERE obs>2 AND timestamp>"+str(start_timestamp)+" INTO OUTFILE '/tmp/id_list.csv' fields terminated by ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'"
	print stmt 
	cursor.execute(stmt)
	# Get the list of addresses
	file_of_addrs = open("/tmp/id_list.csv")
	addrs = file_of_addrs.read().split()
	os.remove('/tmp/id_list.csv')
	return addrs

def walkbys_in_shop(shop_no, cursor):
	cursor.execute("SELECT id, timestamp FROM attendance WHERE rssi<-70 AND sensor_id="+str(shop_no)+" AND timestamp>"+str(start_timestamp)+" GROUP BY id INTO OUTFILE '/tmp/walkbys.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'")
	file_of_walkbys = open("/tmp/walkbys.csv")
	walkbys = file_of_walkbys.read().split()
	os.remove('/tmp/walkbys.csv')
	return walkbys

def behaviour_summary(address, cursor):
	filename = '/tmp/detail.csv'
	sql_command = "SELECT * FROM attendance WHERE id="+addr+" AND timestamp>"+str(start_timestamp)+" ORDER BY timestamp, -rssi INTO OUTFILE '"+filename+"' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'"
	cursor.execute(sql_command)
	print "Getting duration, and inserting to customer_log table."
	g_d = robjects.r('get_duration(\"' + filename + '\")')
	os.remove('/tmp/detail.csv')
	return g_d

def customer_info(mac_addr, outlet):
	try:
		c = Customer.objects.get(mac_addr=eval(addr))
		try:
			Visit.objects.get(patron=c, vendor=outlet)
			first_visit=False
		except (ValueError, ObjectDoesNotExist):
			first_visit=True
	except (ValueError, ObjectDoesNotExist):
		c = Customer(mac_addr=mac_addr)
		c.save()
		first_visit=True
	customer_info = (c, first_visit)
	return customer_info

def month_search(dt, outlet):
	try:
		m= Month.objects.get(vendor=outlet, month_no=dt.month, year=dt.year)
	except (ValueError, ObjectDoesNotExist):
		m = Month(year=dt.year, month_no=dt.month, vendor=outlet, datetime=dt, no_of_walkbys=0, no_of_bounces=0, no_of_entries=0, avg_duration=0)
		m.save()
	return m

def week_search(dt, outlet):
	try:
		w= Week.objects.get(vendor=outlet, week_no=dt.isocalendar()[1], year=dt.year)
	except (ValueError, ObjectDoesNotExist):
		w = Week(datetime=dt, year=dt.year, week_no=dt.isocalendar()[1], vendor=outlet, no_of_walkbys=0, no_of_bounces=0, no_of_entries=0, avg_duration=0)
		w.save()
	return w

def day_search(dt, outlet, week, month):
	try:
		d = Day.objects.get(vendor=outlet, over_week=week, over_month=month)
	except (ValueError, ObjectDoesNotExist):
		d = Day(year=dt.year, month=dt.month, day=dt.day, datetime=dt, over_week=week, over_month=month, vendor=outlet, no_of_walkbys=0, no_of_bounces=0, no_of_entries=0, avg_duration=0)
		d.save()
	return d

def hour_search(dt, day):
	try:
		h = Hour.objects.get(vendor=outlet, day=day, hour=dt.hour)
	except (ValueError, ObjectDoesNotExist):
		h = Hour(datetime=dt, vendor=outlet, day=day, hour=dt.hour, no_of_walkbys=0, no_of_bounces=0, no_of_entries=0, avg_duration=0)
		h.save()
	return h

def time_list(dt, outlet):
	month = month_search(dt, outlet)
	week = week_search(dt, outlet)
	day = day_search(dt, outlet, week, month)
	hour = hour_search(dt, day)
	times = (month, week, day, hour)
	return times


for shop_no in shop_list:
	outlet = Outlet.objects.get(sensor_no=shop_no)
	captures = captures_in_shop(shop_no, cur)
	walkbys = walkbys_in_shop(shop_no, cur)
	Walkby.objects.filter(time__gte=start_timestamp,time__lte=1400000000, vendor=outlet).delete()
	Visit.objects.filter(time__gte=start_timestamp,time__lte=1400000000, vendor=outlet).delete()
	
	for walkby in walkbys:
		entry = walkby.split(',')
		timestamp = int(eval(entry[1]))
		addr = entry[0]
		dt = datetime.fromtimestamp(timestamp, tz=pytz.utc)
		time_tuple = time_list(dt, outlet)
		w = Walkby(addr=eval(addr), vendor=shop, time=timestamp, datetime=dt, month=time_tuple[0], week=time_tuple[1], day=time_tuple[2], hour=time_tuple[3])
		w.save()
		print "Walkby " + str(w.id) + " saved"

	for addr in captures:
		count=0
		c_info = customer_info(addr, outlet)
		g_d = behaviour_summary(addr, cur)
		visits = len(g_d)/4
		timestamp=int(g_d[count+1])
		dt = datetime.fromtimestamp(timestamp, tz=pytz.utc)
		time_tuple = time_list(dt, outlet)
		count = 0
		for i in range(visits):
			v = Visit(patron=c_info[0], vendor=outlet, duration=int(g_d[count+2]), first_visit=c_info[1], month=time_tuple[0], week=time_tuple[1], day=time_tuple[2], hour=time_tuple[3],time=timestamp, datetime=dt)
			v.save()
			count += 4



