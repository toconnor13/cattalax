# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context
from dashboard.models import Day, Hour
import datetime

import time
import random

def get_percentage_graph(x_axis_data, time_periods_to_graph):
	tooltip_date = "%A %d %b"
	ydata = [float(v.get_capture_rate()) for v in time_periods_to_graph]
	ydata2 = [float(v.get_bounce_rate()) for v in time_periods_to_graph]

	extra_serie = {
			"tooltip": {"y_start": "", "y_end": "%"},
			"date_format": tooltip_date
	}

	chartdata = {'x': x_axis_data,
			'name1': 'Capture Rate', 'y1': ydata, 'extra1': extra_serie,
			'name2': 'Bounce Rate', 'y2': ydata2, 'extra2': extra_serie,
	}
	return chartdata

def get_levels_graph(x_axis_data, time_periods_to_graph):
	tooltip_date = "%A %d %b"
	ydata = [float(v.no_of_entries) for v in time_periods_to_graph]
	ydata2 = [float(v.no_of_bounces) for v in time_periods_to_graph]
	ydata3 = [float(v.no_of_walkbys) for v in time_periods_to_graph]

	extra_serie = {
			"tooltip": {"y_start": "Visits: ", "y_end": ""},
		"date_format": tooltip_date
	}
	chartdata = {'x': x_axis_data,
		'name1': 'No. of Walkbys', 'y1': ydata3, 'extra1': extra_serie,
		'name3': 'No. of Captures', 'y3': ydata, 'extra3': extra_serie,
		'name2': 'No. of Bounces', 'y2': ydata2, 'extra2': extra_serie,
	}
	return chartdata

def dashboard(request, levels=False):
	days_to_graph = sorted(Day.objects.all(), key=Day.day_no)
	xdata = map(lambda x: int(time.mktime(datetime.datetime(x.year, x.month, x.day, 12).timetuple())*1000), days_to_graph)

	if levels==False:
		chartdata1 = get_percentage_graph(xdata, days_to_graph)
	else:
		chartdata1 = get_levels_graph(xdata, days_to_graph)

	charttype1 = "lineChart"
	chartcontainer = 'linechart_container' # container name

	data = {
		'charttype1': charttype1,
		'chartdata1': chartdata1, 
		'day_list': days_to_graph,
		'levels' : levels,
		'chartcontainer1': chartcontainer,
		'extra': {
			'x_is_date': True,
			'x_axis_format': '%d %b',
			'tag_script_js': True,
			'jquery_on_ready': False,
		}
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

	if levels==False:
		chartdata1 = get_percentage_graph(xdata, hours_to_show)

	if levels==True:
		chartdata1 = get_levels_graph(xdata, hours_to_show)
	
	chartdata2 = {'x': xdata,
			'name1': 'Duration', 'y1': ydata, 'extra1': extra_serie2,
	}

	charttype1 = "multiBarChart"
	charttype2 = "multiBarChart"

	chartcontainer1 = "multibarchart_container1"
	chartcontainer2 = "multibarchart_container2"

	data = {
		'hour_list': hours_to_show,
		'charttype1': charttype1,
		'chartdata1': chartdata1,
		'chartcontainer1': chartcontainer1,
		'charttype2': charttype2,
		'chartdata2': chartdata2,
		'chartcontainer2': chartcontainer2,
		'day': d,
		'levels': levels,
		'extra': {
			'x_is_date': False,
			'x_axis_format': '',
			'tag_script_js': True,
			'jquery_on_ready': True
		}
	}

	return render_to_response('dashboard/detail.html', data, context_instance=RequestContext(request))


def contact(request):
	path = request.path
	return render_to_response('contact.html', {'path':path}, context_instance=RequestContext(request))
