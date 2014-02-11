from django.db import models
from datetime import datetime
from datetime import timedelta

class Customer(models.Model):
	mac_addr = models.CharField(max_length=300)

	def __unicode__(self):
		return self.mac_addr

class Outlet(models.Model):
	name    = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	city    = models.CharField(max_length=20)
	county  = models.CharField(max_length=20)
	agent   = models.CharField(max_length=30)
	sensor_no = models.IntegerField()

	def __unicode__(self):
		return self.name


class TimeUnit(models.Model):
	vendor = models.ForeignKey(Outlet)
	no_of_walkbys = models.IntegerField()
	no_of_entries = models.IntegerField()
	no_of_bounces = models.IntegerField()
	avg_duration = models.IntegerField()
	datetime = models.DateTimeField()

	class Meta:
		abstract = True

	def get_capture_rate(self):
		if (self.no_of_walkbys==0):
			return '0'
		else:
			rate =  float(self.no_of_entries)*100/float(self.no_of_walkbys)
			return str(round(rate,1))

	def get_bounce_rate(self):
		if self.no_of_entries==0:
			return '0'
		else:
			rate = float(self.no_of_bounces)*100/float(self.no_of_entries)
			return str(round(rate,1))

	def get_avg_duration(self):
		mins = self.avg_duration / 60
		secs = self.avg_duration % 60
		if secs<10:
			seconds = '0' + str(secs)
		else:
			seconds = str(secs)
		return str(mins) + ':' + seconds

	def percent_of_new_customers(self):
		total_customers = len(set([v.patron for v in self.visit_set.all()]))
		total_new_customers = len(set([v.patron for v in self.visit_set.all() if v.first_visit==True]))
		percent = float(total_customers)*100/float(total_new_customers)
		return percent


class Month(TimeUnit):
	year = models.IntegerField()
	month_no = models.IntegerField()
	
	def describe(self):
		return self.datetime.strftime("%B %Y")


class Week(TimeUnit):
	year = models.IntegerField()
	week_no = models.IntegerField()
	def describe(self):
		date_to_describe = self.datetime - timedelta(days=5) 
		return date_to_describe.strftime("%a %d %b")

class Day(TimeUnit):
	day = models.IntegerField()
	month = models.IntegerField()
	year = models.IntegerField()
	over_month = models.ForeignKey(Month)
	over_week = models.ForeignKey(Week)

	def day_no(self):
		return int(self.day)

	def describe(self):
		return self.datetime.strftime("%a %d %b")

	def print_day(self):
		return self.datetime.strftime("%a %d")

	def print_month(self):
		return self.datetime.strftime("%B %Y")
	
class Hour(TimeUnit):
	hour = models.IntegerField()
	day = models.ForeignKey(Day)

	def describe(self):
		return self.datetime.strftime("%H:%M") # prepend %A for day string

class Encounter(models.Model):
	vendor = models.ForeignKey(Outlet)
	time = models.IntegerField()
	datetime = models.DateTimeField()

	class Meta:
		abstract=True

	def get_hour(self):
		return datetime.hour

class Visit(Encounter):
	patron = models.ForeignKey(Customer)
	hour = models.ForeignKey(Hour)
	day = models.ForeignKey(Day)
	duration = models.IntegerField()
	first_visit = models.BooleanField()

class Walkby(Encounter):
	"Nothing here."	

