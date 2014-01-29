# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context
from dashboard.models import Day, Hour, Outlet
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import datetime
import re
import time
import random

def perdelta(start, end, delta):
	cur = start
	while cur <= end:
		yield cur
		cur += delta

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
				dict_names[0]: 'Walkbys',
				dict_names[1]: [float(v.no_of_walkbys) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		elif i==2:
			new_dict = {
				dict_names[0]: 'Captures',
				dict_names[1]: [float(v.no_of_entries) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		elif i==3:
			new_dict = {
				dict_names[0]: 'Bounces',
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

		elif i==6:
			new_dict = {
				dict_names[0]: 'Duration',
				dict_names[1]: [float(v.avg_duration) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
	
		chartdata = dict(chartdata.items() + new_dict.items())	
	return chartdata



def create_graph(x_axis_data, objects_to_graph, charttype, chartcontainer, levels=False, graph_no=1, x_is_date=True, x_format='%d %b', non_level=False, var_list=[]):
	if non_level==False:
		if levels==False:
			chartdata = get_chartdata(x_axis_data, objects_to_graph, [4,5])	
		else:
			chartdata = get_chartdata(x_axis_data, objects_to_graph, [1,2,3])
	else:
		chartdata = get_chartdata(x_axis_data, objects_to_graph, var_list)
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
				'x_is_date': x_is_date,			
				'x_axis_format': x_format,
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

def get_days_to_show(start_date, end_date, days_to_graph):
	days_to_show = []
	for date in perdelta(start_date, end_date, datetime.timedelta(days=1)):
		try:
			day = days_to_graph.get(year=date.year, month=date.month, day=date.day)
			days_to_show.append(day)
		except:
			pass
	return days_to_show

#	days_to_graph = sorted(Day.objects.all(), key=Day.day_no)
#	days_to_show = sorted(days_to_show, key=lambda day: day.day_no)


@login_required
def dashboard(request):
	nav="dashboard"
	request.session['nav']= nav
	vendor_username = request.user.username
	outlet_list = Outlet.objects.all() # filter(agent=vendor_username)
	pattern = '(\d\d)/(\d\d)/(\d\d\d\d)'
	if request.method=='POST':
		start = request.POST['start']
		end = request.POST['end']
		focus = request.POST['focus']
		shop_id = request.POST['shop_id']
	else:
		start = '08/24/2015'
		end = '08/30/2015'
		focus = "day"
		shop_id = outlet_list[0].sensor_no
	vendor = outlet_list.get(sensor_no=shop_id) 
	days_to_graph = Day.objects.filter(vendor=vendor)

	# Interpret the dates
	start_match = re.match(pattern, start)
	end_match = re.match(pattern, end)
	start_date = datetime.date(int(start_match.group(3)), int(start_match.group(1)), int(start_match.group(2)))
	end_date = datetime.date(int(end_match.group(3)), int(end_match.group(1)), int(end_match.group(2)))

		
	# Generate the graphs
	if focus=="day":
		days_to_show = get_days_to_show(start_date, end_date, days_to_graph)
		xdata = map(lambda x: int(time.mktime(datetime.datetime(x.year, x.month, x.day, 12).timetuple())*1000), days_to_show)
		data1 = create_graph(xdata, days_to_show, 'lineChart', 'linechart_container1', levels=False, graph_no=1)
		data2 = create_graph(xdata, days_to_show, 'lineChart', 'linechart_container2', levels=True, graph_no=2)

	# Gather the data and return it
	data = dict(data1.items()+ data2.items() +[('outlet_list', outlet_list)])

	# Set the session data so the information will be carried to the form
	request.session['start'] = start
	request.session['end'] = end
	request.session['focus'] = focus
	request.session['shop_id'] = shop_id
	return render_to_response('dashboard/index.html', data, context_instance=RequestContext(request))

@login_required
def detail(request, day_id, levels=False):
	vendor_username = request.user.username
#	outlet_list = Outlet.objects.filter(agent=vendor_username)
	outlet_list = Outlet.objects.all()
	d = get_object_or_404(Day, pk=day_id)
	if d.vendor not in outlet_list:
		return HttpResponseRedirect('/dashboard')
	start = '08/24/2015'
	end = '08/30/2015'
	hours_to_show = [h for h in d.hour_set.all() if h.hour>6 and h.hour<20]
	xdata = map(lambda h: str(h.hour), hours_to_show)
	chartdata1 = create_graph(xdata, hours_to_show, 'multiBarChart', 'multibarchart_container1', levels, graph_no=1, x_is_date=False, x_format='')
	chartdata2 = create_graph(xdata, hours_to_show, 'multiBarChart', 'multibarchart_container2', graph_no=2, non_level=True, var_list=[6])
	data = dict( chartdata1.items() + chartdata2.items() + [('end',end), ('day', d), ('outlet_list', outlet_list)])
	return render_to_response('dashboard/detail.html', data, context_instance=RequestContext(request))

def contact(request):
	path = request.path
	return render_to_response('contact.html', {'path':path}, context_instance=RequestContext(request))

def data(request):
	path = request.path
	return render_to_response('data.html', {'path':path}, context_instance=RequestContext(request))


def opt_out(request):
	message = "The MAC Address has successfully been submitted."
	mac_addr_submitted = False
	if request.method=='POST':
		mac_addr = request.POST['mac_addr']
		mac_addr_submitted = True
		print mac_addr
	return render_to_response('opt-out.html', {'message': message, 'submitted': mac_addr_submitted}, context_instance=RequestContext(request))

def campaigns(request):
	request.session['nav']="campaigns"
	return render_to_response('dashboard/campaigns.html', context_instance=RequestContext(request))

def campaign_form(request):
	return render_to_response('dashboard/campaign_form.html', context_instance=RequestContext(request))

def details(request):
	request.session['nav']="details"
	return render_to_response('dashboard/user_details.html', context_instance=RequestContext(request))

def event(request):
	return render_to_response('dashboard/event.html', context_instance=RequestContext(request))
