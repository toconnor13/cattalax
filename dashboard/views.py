# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context
from dashboard.models import Day, Hour
import datetime

import time
import random


def get_chartdata(x_axis_data, time_periods_to_graph, vars_to_graph):
	tooltip_date = "%A %d %b"
	no_of_vars = len(vars_to_graph)
	chartdata = {'x': x_axis_data,}
	
	extra_serie = {
		"tooltip": {"y_start": "Visits: ", "y_end": ""},
		"date_format": tooltip_date
	}

	graph_att = ['name', 'y', 'extra']

	for i in vars_to_graph:
		index = i+1
		dict_names = [att+str(index) for att in graph_att]
		if i==1:
			new_dict = {
				dict_names[0]: 'No. of Walkbys',
				dict_names[1]: [float(v.no_of_walkbys) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		elif i==2:
			new_dict = {
				dict_names[0]: 'No. of Captures',
				dict_names[1]: [float(v.no_of_entries) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		elif i==3:
			new_dict = {
				dict_names[0]: 'No. of Bounces',
				dict_names[1]: [float(v.no_of_bounces) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		elif i==4:
			new_dict = {
				dict_names[0]: 'Capture Rate',
				dict_names[1]: [float(v.get_capture_rate()) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		elif i==5:
			new_dict = {
				dict_names[0]: 'Bounce Rate',
				dict_names[1]: [float(v.get_bounce_rate()) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}

		elif index==6:
			new_dict = {
				dict_names[0]: 'Duration',
				dict_names[1]: [float(v.no_of_captures) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
	
		chartdata = dict(chartdata.items() + new_dict.items())	
	return chartdata



def create_graph(x_axis_data, objects_to_graph, charttype, chartcontainer, levels=False, graph_no=1):
	if levels==False:
		chartdata = get_chartdata(x_axis_data, objects_to_graph, [4,5])	
	else:
		chartdata = get_chartdata(x_axis_data, objects_to_graph, [1,2,3])
	dict_items = ['charttype', 'chartdata', 'chartcontainer']
	var_names = [i + str(graph_no) for i in dict_items]
	if graph_no==1:
		data = {
			var_names[0]: charttype, 
			var_names[1]: chartdata,
			var_names[2]: chartcontainer,
			'object_list': objects_to_graph,
			'levels': levels,
			'extra': {
				'x_is_date': True,			
				'x_axis_format': '%d %b',
				'tag_script_js': True,
				'jquery_on_ready': False,
			}
		}
	else:
		data = { 
			var_names[0]: charttype, 
			var_names[1]: chartdata,
			var_names[2]: chartcontainer,
		}
	return data


def dashboard(request, levels=False):
	days_to_graph = sorted(Day.objects.all(), key=Day.day_no)
	xdata = map(lambda x: int(time.mktime(datetime.datetime(x.year, x.month, x.day, 12).timetuple())*1000), days_to_graph)
	data = create_graph(xdata, days_to_graph, 'lineChart', 'linechart_container', levels, 1)

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

	chartdata1 = create_graph(xdata, hours_to_show, 'multiBarChart', 'multibarchart_container1', levels, 1)

#	if levels==False:
#		chartdata1 = get_percentage_graph(xdata, hours_to_show)
#
#	if levels==True:
#		chartdata1 = get_levels_graph(xdata, hours_to_show)
	
	chartdata2 = {'x': xdata,
			'name1': 'Duration', 'y1': ydata, 'extra1': extra_serie2,
	}

	charttype1 = "multiBarChart"
	charttype2 = "multiBarChart"

	chartcontainer1 = "multibarchart_container1"
	chartcontainer2 = "multibarchart_container2"

	data = {
		'hour_list': hours_to_show,
#		'charttype1': charttype1,
#		'chartdata1': chartdata1,
#		'chartcontainer1': chartcontainer1,
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
	data = dict(data.items() + chartdata1.items())

	return render_to_response('dashboard/detail.html', data, context_instance=RequestContext(request))


def contact(request):
	path = request.path
	return render_to_response('contact.html', {'path':path}, context_instance=RequestContext(request))
