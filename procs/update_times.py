import os, sys

path='/root/.virtualenvs/cattalax/cattalax'
if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]="cattalax.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cattalax.settings") 

from django.utils import timezone
from dashboard.models import *
import datetime

list_of_shops = [v for v in Outlet.objects.all()]

def compute(time):
	list_of_visits = [visit for visit in time.visit_set.all()]
	time.no_of_entries = len(list_of_visits)

	list_of_walkbys = [walkby for walkby in time.walkby_set.all()]
	time.no_of_walkbys = len(list_of_walkbys)

	list_of_bounces = [v for v in list_of_visits if v.duration<60]
	time.no_of_bounces = len(list_of_bounces)

	if time.no_of_entries>0:
		time.avg_duration = sum([int(v.duration) for v in list_of_visits])/time.no_of_entries

	time.save()


for shop in list_of_shops:
	months_to_update = shop.month_set.filter(datetime__gte=timezone.now()-datetime.timedelta(days=7))
	weeks_to_update = shop.week_set.filter(datetime__gte=timezone.now()-datetime.timedelta(days=7))
	days_to_update = shop.day_set.filter(datetime__gte=timezone.now()-datetime.timedelta(days=7))	

	for month in months_to_update:
		compute(month)
	for week in weeks_to_update:
		compute(week)

	for day in days_to_update:
		compute(day)	
		for hour in day.hour_set.all():
			compute(hour)	

