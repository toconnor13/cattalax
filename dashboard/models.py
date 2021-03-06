from django.db import models
from datetime import datetime
from datetime import timedelta

class Customer(models.Model):
	mac_addr = models.CharField(max_length=300)
	tag = models.CharField(max_length=100)

	def __unicode__(self):
		return self.mac_addr

class Opt_out(models.Model):
	mac_addr = models.CharField(max_length=50)

	def __unicode__(self):
		return self.mac_addr

class Outlet(models.Model):
	name    = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	city    = models.CharField(max_length=20)
	county  = models.CharField(max_length=20)
	agent   = models.CharField(max_length=30)
	sensor_no = models.IntegerField()
	outer_bound = models.IntegerField()
	inner_bound = models.IntegerField()

	def __unicode__(self):
		return self.name

class Campaign(models.Model):
	outlet = models.ForeignKey(Outlet)
	name = models.CharField(max_length=300)
	start = models.DateTimeField()
	end = models.DateTimeField()
	category = models.IntegerField()

	def capture_rate_effect(self):
		effect = 13
		return effect
	def bounce_rate_effect(self):
		effect = -9
		return effect
	def duration_effect(self):
		effect =134
		return effect
	def frequency_effect(self):
		effect = 2
		return effect

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
		if self.no_of_walkbys==0 and self.no_of_entries>0:
			return '100'
		elif self.no_of_walkbys==0 and self.no_of_entries==0:
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
		visit_list = self.visit_set.all().filter(hour__hour__gte=8, hour__hour__lte=20)
		total_customers = len(set([v.patron for v in visit_list]))
		total_new_customers = len(set([v.patron for v in visit_list if v.first_visit==True]))
		if total_customers==0:
			return 0
		else:
			percent = float(total_new_customers)*100/float(total_customers)
			return percent

class Month(TimeUnit):
	year = models.IntegerField()
	month_no = models.IntegerField()
	
	def describe(self):
		return self.datetime.strftime("%B %Y")

	def print_self(self):
		return self.datetime.strftime("%B")

	def print_container(self):
		return self.datetime.strftime("%Y")



class Week(TimeUnit):
	year = models.IntegerField()
	week_no = models.IntegerField()

	def describe(self):
		days_into_week = self.datetime.isocalendar()[2]
		start_of_week = self.datetime - timedelta(days=days_into_week-1)
		return start_of_week.strftime("%a %d %b")

	def print_self(self):
		days_into_week = self.datetime.isocalendar()[2]
		start_of_week = self.datetime - timedelta(days=days_into_week-1)
		description = "Week of " + start_of_week.strftime("%a %d %b")
		return description

	def print_container(self):
		return self.datetime.strftime("%B %Y")

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

	def print_self(self):
		return self.datetime.strftime("%a %d")

	def print_container(self):
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
	month = models.ForeignKey(Month)
	week = models.ForeignKey(Week)
	day = models.ForeignKey(Day)
	hour = models.ForeignKey(Hour)
	
	class Meta:
		abstract=True

	def get_hour(self):
		return datetime.hour

class Visit(Encounter):
	duration = models.IntegerField()
	first_visit = models.BooleanField()
	patron = models.ForeignKey(Customer)

class Walkby(Encounter):
	addr = models.CharField(max_length=300)

