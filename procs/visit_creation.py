import os, sys
import MySQLdb
import calendar
import pytz
import hashlib
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from duration import *

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


def calculate_view(shop, start_time, cursor):
	view_name = "capture"+str(shop.sensor_no)
	cursor.execute("CREATE OR REPLACE VIEW "+view_name+" AS SELECT DISTINCT id, timestamp, count(id) AS obs FROM attendance WHERE sensor_id="+str(shop.sensor_no)+" AND timestamp>"+str(start_time)+" AND rssi>"+str(shop.inner_bound)+" GROUP BY id")
	return view_name

def captures_in_shop(shop, cursor, t0_stamp, t1_stamp):
	view = calculate_view(shop, t0_stamp, cursor)

	stmt = "SELECT id FROM "+view+" WHERE timestamp>"+str(t0_stamp)+" AND timestamp<"+ str(t1_stamp)+" INTO OUTFILE '/tmp/id_list.csv' fields terminated by ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'"
#	print stmt 
	cursor.execute(stmt)
	# Get the list of addresses
	file_of_addrs = open("/tmp/id_list.csv")
	addrs = file_of_addrs.read().split()
	os.remove('/tmp/id_list.csv')
	return addrs

def walkbys_in_shop(shop, cursor, t0_stamp, t1_stamp):
	cursor.execute("SELECT id, timestamp FROM attendance WHERE rssi>"+str(shop.outer_bound)+" AND sensor_id="+str(shop.sensor_no)+" AND timestamp>"+str(t0_stamp)+" AND timestamp<"+str(t1_stamp)+" GROUP BY id INTO OUTFILE '/tmp/walkbys.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'")
	file_of_walkbys = open("/tmp/walkbys.csv")
	walkbys = file_of_walkbys.read().split()
	os.remove('/tmp/walkbys.csv')
	return walkbys

def behaviour_summary(addr, cursor, outlet, t0_stamp, t1_stamp):
	filename = '/tmp/detail.csv'
	sql_command = "SELECT * FROM attendance WHERE id="+addr+" AND timestamp>"+str(t0_stamp)+" AND timestamp<"+str(t1_stamp)+" ORDER BY timestamp, -rssi INTO OUTFILE '"+filename+"' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'"
	cursor.execute(sql_command)
	if os.stat(filename).st_size<500000:
		g_d = robjects.r('get_duration(\"' + filename + '\",'+str(outlet.inner_bound)+')')
	else:
		g_d = [0,0,0,0]
	os.remove('/tmp/detail.csv')
	return g_d

def customer_info(mac_addr):
	try:
		c = Customer.objects.get(mac_addr=eval(mac_addr))
	except (ValueError, ObjectDoesNotExist):
		c = Customer(mac_addr=eval(mac_addr))
		c.save()
	return c

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
		d = Day.objects.get(vendor=outlet, over_week=week, over_month=month, day=dt.day)
	except (ValueError, ObjectDoesNotExist):
		d = Day(year=dt.year, month=dt.month, day=dt.day, datetime=dt, over_week=week, over_month=month, vendor=outlet, no_of_walkbys=0, no_of_bounces=0, no_of_entries=0, avg_duration=0)
		d.save()
	return d

def hour_search(dt, day, outlet):
	try:
		h = Hour.objects.get(day=day, hour=dt.hour)
	except (ValueError, ObjectDoesNotExist):
		h = Hour(datetime=dt, vendor=outlet, day=day, hour=dt.hour, no_of_walkbys=0, no_of_bounces=0, no_of_entries=0, avg_duration=0)
		h.save()
	return h

def time_list(dt, outlet):
	month = month_search(dt, outlet)
	week = week_search(dt, outlet)
	day = day_search(dt, outlet, week, month)
	hour = hour_search(dt, day, outlet)
	times = (month, week, day, hour)
	return times

def compute(time):
	list_of_visits = [v for v in time.visit_set.all().filter(hour__hour__gte=7, hour__hour__lte=19)]
	time.no_of_entries = len(list_of_visits)

	list_of_walkbys = [w for w in time.walkby_set.all().filter(hour__hour__gte=7, hour__hour__lte=19)]
	time.no_of_walkbys = len(list_of_walkbys)

	list_of_bounces = [v for v in list_of_visits if v.duration<60]
	time.no_of_bounces = len(list_of_bounces)

	if time.no_of_entries>0:
		time.avg_duration = sum([int(v.duration) for v in list_of_visits])/time.no_of_entries
	else:
		time.avg_duration=0
	time.save()
#	print "Updating "+str(time.datetime)


def is_first_visit(c, outlet):
	vl = Visit.objects.filter(patron=c, vendor=outlet)
	if len(vl)>0:
		first_visit=False
	else:
		first_visit=True
	return first_visit

def record_walkby(walkby, shop):
	entry = walkby.split(',')
	timestamp = int(eval(entry[1]))
	addr = hashlib.sha224(eval(entry[0])).hexdigest() # Hash the address here
	dt = datetime.fromtimestamp(timestamp, tz=pytz.utc)
	time_tuple = time_list(dt, shop)
	w = Walkby(addr=addr, vendor=shop, time=timestamp, datetime=dt, month=time_tuple[0], week=time_tuple[1], day=time_tuple[2], hour=time_tuple[3])
	w.save()
#	print "Walkby " + str(w.id) + " saved"

def record_capture(addr, shop, cursor, t0_stamp, t1_stamp):
	count=0
	# Hash the address here
	addr = hashlib.sha224(addr).hexdigest()
	c_info = customer_info(addr)
	g_d = behaviour_summary(addr, cursor, shop, t0_stamp, t1_stamp)
	visits = len(g_d)/4
	timestamp=int(g_d[count+1])
	dt = datetime.fromtimestamp(timestamp, tz=pytz.utc)
	time_tuple = time_list(dt, shop)
	count = 0
	for i in range(visits):
		first_visit= is_first_visit(c_info, shop)
		v = Visit(patron=c_info, vendor=shop, duration=int(g_d[count+2]), first_visit=first_visit, month=time_tuple[0], week=time_tuple[1], day=time_tuple[2], hour=time_tuple[3],time=timestamp, datetime=dt)
		v.save()
	#	print "A visit "+str(v.patron.mac_addr)+" saved"
		count += 4

def analyse_shop(shop, cursor, t0, t1):
	t0_stamp = calendar.timegm(t0.utctimetuple())
	t1_stamp = calendar.timegm(t1.utctimetuple())
	captures = captures_in_shop(shop, cursor, t0_stamp, t1_stamp)
	walkbys = walkbys_in_shop(shop, cursor, t0_stamp, t1_stamp)
#	Walkby.objects.filter(time__gte=t0_stamp, time__lte=t1_stamp, vendor=shop).delete()
#	Visit.objects.filter(time__gte=t0_stamp, time__lte=t1_stamp, vendor=shop).delete()
#	Week.objects.filter(datetime__gte=t0, datetime__lte=t1, vendor=shop).delete()
	
	for walkby in walkbys:
		record_walkby(walkby, shop)
	for addr in captures:
		record_capture(addr, shop, cursor, t0_stamp, t1_stamp)
		

#	months_to_update = shop.month_set.filter(datetime__gte=t0, datetime__lte=t1)
	months_to_update = shop.month_set.all()
	weeks_to_update = shop.week_set.filter(datetime__gte=t0, datetime__lte=t1)
	days_to_update = shop.day_set.filter(datetime__gte=t0, datetime__lte=t1)

	for month in months_to_update:
		compute(month)
	for week in weeks_to_update:
		compute(week)
	for day in days_to_update:
		compute(day)
		for hour in day.hour_set.all():
			compute(hour)

shop_list = [shop for shop in Outlet.objects.all()]
t1 = timezone.now()
no_of_days=2
t0 = t1 - timedelta(days=no_of_days)
dt = datetime(year=t1.year, month=t1.month, day=t1.day, tzinfo=pytz.utc)
dt_list = []

for i in range(no_of_days):
	dt_to_add = dt -timedelta(days=i)
	dt_list.append(dt_to_add)

for shop in shop_list:
	analyse_shop(shop, cur, dt_list[0], t1)
	for i in range(no_of_days-1):
		analyse_shop(shop, cur, dt_list[i+1], dt_list[i])



