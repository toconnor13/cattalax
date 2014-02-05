from django.db import models
from datetime import datetime

# Create your models here.
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


# class Month:
	

#class Week (models.Model):
class TimeUnit(models.Model):
	vendor = models.ForeignKey(Outlet)
	no_of_walkbys = models.IntegerField()
	no_of_entries = models.IntegerField()
	no_of_bounces = models.IntegerField()
	avg_duration = models.IntegerField()
	# some datetime object?	
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
	
class Day(TimeUnit):
	day = models.IntegerField()
	month = models.IntegerField()
	year = models.IntegerField()
	# a datetime object could combine the above three

	def day_no(self):
		return int(self.day)

	def describe(self):
		d = datetime(self.year, self.month, self.day)
		return d.strftime("%a %d %b")

	def print_day(self):
		d = datetime(self.year, self.month, self.day)
		return d.strftime("%a %d")

	def print_month(self):
		d = datetime(self.year, self.month, self.day)
		return d.strftime("%B %Y")
	
class Hour(TimeUnit):
	hour = models.IntegerField()
	day = models.ForeignKey(Day)

	def describe(self):
		d = datetime(self.day.year, self.day.month, self.day.day, self.hour)
		return d.strftime("%H:%M") # prepend %A for day string

class Encounter(models.Model):
	vendor = models.ForeignKey(Outlet)
	time = models.IntegerField()
#	day = models.ForeignKey(Day)
#	datetime = models.DateTimeField(null=True)
#	week = models.ForeignKey(Week)
#	month = models.ForeignKey(Month)
	class Meta:
		abstract=True

class Visit(Encounter):
	patron = models.ForeignKey(Customer)
	duration = models.IntegerField()
	# A field is need here to attach the visit to an hour or day.  Preferably hour, but day will need to count the visits over all its children.
	# arrival_time datetime field
	# day foreign key field
	# week foreign key field
	# month foreign key field

	def get_hour(self):
		t = datetime.fromtimestamp(self.arrival_time)
		return t.hour

class Walkby(Encounter):
	# time datetime field
	# day foreign key field
	# week foreign key field
	# month foreign key field
	
	def get_hour(self):
		t = datetime.fromtimestamp(self.time)
		return t.hour

