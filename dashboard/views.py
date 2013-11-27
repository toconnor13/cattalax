# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context
from dashboard.models import Day, Hour
import datetime

import time
import random

def dashboard(request, levels=False):
	days_to_graph = sorted(Day.objects.all(), key=Day.day_no)
	xdata = map(lambda x: int(time.mktime(datetime.datetime(x.year, x.month, x.day, 12).timetuple())*1000), days_to_graph)
	
	
	tooltip_date = "%A %d %b" 

	if levels==False:
		ydata = [float(v.get_capture_rate()) for v in days_to_graph]
		ydata2 = [float(v.get_bounce_rate()) for v in days_to_graph]

		extra_serie = {
			"tooltip": {"y_start": "", "y_end": "%"},
			"date_format": tooltip_date
		}

		chartdata1 = {'x': xdata, 
			'name1': 'Capture Rate', 'y1': ydata, 'extra1': extra_serie,
			'name2': 'Bounce Rate', 'y2': ydata2, 'extra2': extra_serie,
		}
	else:
		ydata = [float(v.no_of_entries) for v in days_to_graph]
		ydata2 = [float(v.no_of_bounces) for v in days_to_graph]
		ydata3 = [float(v.no_of_walkbys) for v in days_to_graph]

		extra_serie = {
		#	"tooltip": {"y_start": "", "y_end": ""},
			"date_format": tooltip_date
		}


		chartdata1 = {'x': xdata, 
			'name1': 'No. of Walkbys', 'y1': ydata3, 'extra1': extra_serie,
			'name3': 'No. of Captures', 'y3': ydata, 'extra3': extra_serie,
			'name2': 'No. of Bounces', 'y2': ydata2, 'extra2': extra_serie,
		}


	charttype1 = "lineChart"

	data = {
		'charttype1': charttype1,
		'chartdata1': chartdata1, 
		'day_list': days_to_graph,
		'levels' : levels,
		}

	return render_to_response('dashboard/index.html', data, context_instance=RequestContext(request))


def detail(request, day_id, levels=False):
	d = get_object_or_404(Day, pk=day_id)

	hours_to_show = [h for h in d.hour_set.all() if h.hour>6 and h.hour<20]
	xdata = map(lambda h: str(h.hour), hours_to_show)

	ydata = [v.avg_duration for v in hours_to_show]
	
	tooltip_date = "%A %d %b"
	extra_serie2 = {
		"tooltip": {"y_start": "", "y_end": " seconds"},
		"date_format": tooltip_date,
	}

	extra_serie1 = {
		"tooltip": {"y_start": "", "y_end": "%"},
		"date_format": tooltip_date,
	}

	if levels==False:
		ydata2 = [float(v.get_capture_rate()) for v in hours_to_show]
		ydata3 = [float(v.get_bounce_rate()) for v in hours_to_show]

		chartdata1 = {'x': xdata, 
			'name1': 'Capture Rate', 'y1': ydata2, 'extra1': extra_serie1,
			'name2': 'Bounce Rate', 'y2': ydata3, 'extra2': extra_serie1,
		}

	if levels==True:
		ydata2 = [float(v.no_of_entries) for v in hours_to_show]
		ydata3 = [float(v.no_of_walkbys) for v in hours_to_show]
		ydata4 = [float(v.no_of_bounces) for v in hours_to_show]

		chartdata1 = {'x': xdata, 
			'name1': 'No. of Walkbys', 'y1': ydata3,# 'extra1': extra_serie2
			'name3': 'No. of Captures', 'y3': ydata2,# 'extra3': extra_serie,
			'name2': 'No. of Bounces', 'y2': ydata4,# 'extra2': extra_serie,
		}

	
	
	chartdata2 = {'x': xdata,
			'name1': 'Duration', 'y1': ydata, 'extra1': extra_serie2,
	}

	charttype1 = "multiBarChart"
	charttype2 = "multiBarChart"


	data = {
		'hour_list': hours_to_show,
		'charttype1': charttype1,
		'chartdata1': chartdata1,
		'charttype2': charttype2,
		'chartdata2': chartdata2,
		'day': d,
		'levels': levels,
	}

	return render_to_response('dashboard/detail.html', data, context_instance=RequestContext(request))


def contact(request):
	path = request.path
	return render_to_response('contact.html', {'path':path}, context_instance=RequestContext(request))
