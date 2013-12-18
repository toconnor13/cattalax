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

class Visit(models.Model):
	patron = models.ForeignKey(Customer)
	vendor = models.ForeignKey(Outlet)
	duration = models.IntegerField()
	arrival_time = models.IntegerField()

	def get_hour(self):
		t = datetime.fromtimestamp(self.arrival_time)
		return t.hour
	

class Walkby(models.Model):
	vendor = models.ForeignKey(Outlet)
	time = models.IntegerField()
	
	def get_hour(self):
		t = datetime.fromtimestamp(self.time)
		return t.hour


class Day(models.Model):
	vendor = models.ForeignKey(Outlet)
	day = models.IntegerField()
	month = models.IntegerField()
	year = models.IntegerField()
	no_of_walkbys = models.IntegerField()
	no_of_entries = models.IntegerField()
	no_of_bounces = models.IntegerField()
	avg_duration = models.IntegerField()

	def day_no(self):
		return int(self.day)

	def get_day_string(self):
		d = datetime(self.year, self.month, self.day)
		return d.strftime("%a %d %b")
	
	def get_capture_rate(self):
		rate =  float(self.no_of_entries)*100/float(self.no_of_walkbys)
		return str(round(rate,1)) 

	def get_bounce_rate(self):
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

class Hour(models.Model):
	hour = models.IntegerField()
	day = models.ForeignKey(Day)
	vendor = models.ForeignKey(Outlet)
	no_of_walkbys = models.IntegerField()
	no_of_entries = models.IntegerField()
	no_of_bounces = models.IntegerField()
	avg_duration = models.IntegerField()

	def get_hour_string(self):
		d = datetime(self.day.year, self.day.month, self.day.day, self.hour)
		return d.strftime("%A %H:%M")

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


