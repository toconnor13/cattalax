# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context
from dashboard.models import Month, Week, Day, Hour, Outlet, Campaign
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

def get_chartdata(x_axis_data, time_periods_to_graph, vars_to_graph, y_start="", y_end="%"):
	tooltip_date = "%A %d %b"
	no_of_vars = len(vars_to_graph)
	chartdata = {'x': x_axis_data,}
	
	extra_serie = {
		"tooltip": {"y_start": y_start, "y_end": y_end},
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
				dict_names[0]: 'Capture %',
				dict_names[1]: [float(v.get_capture_rate()) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		elif i==5:
			new_dict = {
				dict_names[0]: 'Bounce %',
				dict_names[1]: [float(v.get_bounce_rate()) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		elif i==6:
			new_dict = {
				dict_names[0]: 'Duration',
				dict_names[1]: [float(v.avg_duration) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		elif i==7:
			new_dict = {
				dict_names[0]: 'New Customers %',
				dict_names[1]: [int(v.percent_of_new_customers()) for v in time_periods_to_graph],
				dict_names[2]: extra_serie,
			}
		chartdata = dict(chartdata.items() + new_dict.items())	
	return chartdata

def create_graph(x_axis_data, objects_to_graph, charttype, chartcontainer, levels=False, graph_no=1, x_is_date=True, x_format='%d %b', non_level=False, var_list=[], y_start="", y_end="%"):
	if non_level==False:
		if levels==False:
			chartdata = get_chartdata(x_axis_data, objects_to_graph, [4,5,7], y_start, y_end)	
		else:
			chartdata = get_chartdata(x_axis_data, objects_to_graph, [1,2,3], y_start, y_end)
	else:
		chartdata = get_chartdata(x_axis_data, objects_to_graph, var_list, y_start, y_end=" seconds")
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
		objects_to_show = get_days_to_show(start_date, end_date, days_to_graph)
		xdata = map(lambda x: int(time.mktime(x.datetime.timetuple())*1000), objects_to_show)
	elif focus=="week":
		objects_to_show = Week.objects.all()
		xdata = map(lambda x: int(time.mktime(x.datetime.timetuple())*1000), objects_to_show)
	else:
		objects_to_show = Month.objects.all()
		xdata = map(lambda x: int(time.mktime(x.datetime.timetuple())*1000), objects_to_show)
	data1 = create_graph(xdata, objects_to_show, 'lineChart', 'linechart_container1', levels=False, graph_no=1)
	data2 = create_graph(xdata, objects_to_show, 'lineChart', 'linechart_container2', levels=True, graph_no=2)


	# Gather the data and return it
	data = dict(data1.items()+ data2.items() +[('outlet_list', outlet_list)])

	# Set the session data so the information will be carried to the form
	request.session['start'] = start
	request.session['end'] = end
	request.session['focus'] = focus
	request.session['shop_id'] = shop_id
	return render_to_response('dashboard/index.html', data, context_instance=RequestContext(request))

def customer_piechart(time):
	xdata3 = ["New", "Return"]
	new_percent = int(time.percent_of_new_customers())
	old_percent = 100-new_percent
	ydata3 = [new_percent, old_percent]
	extra_serie = {"tooltip": {"y_start": "", "y_end": "%"}}
	chartdata = {
			'x': xdata3,
			'y1': ydata3,
			'extra1': extra_serie
		}
	charttype="pieChart"
	data = {
		'charttype3': charttype,
		'chartdata3': chartdata,
		'chartcontainer3': "piechart_container"
		}
	return data

def duration_bin(time):
	xdata = ["0-5", "5-10", "10-20", "20-30", "30-60", "60+"]
	ydata = [0, 0, 0, 0, 0, 0]
	visits = time.visit_set.all()
	duration_list = [v.duration for v in visits]
	for duration in duration_list:
		if duration < 300:
			ydata[0]+= 1
		elif duration>300 and duration<600:
			ydata[1]+=1
		elif duration>600 and duration<1200:
			ydata[2]+=1
		elif duration>1200 and duration<1800:
			ydata[3]+=1
		elif duration>1800 and duration<3600:
			ydata[4]+=1
		elif duration>3600:
			ydata[5]+=1
	extra_serie1 = {"tooltip": {"y_start": "", "y_end": " visits"}}
	chartdata = {
		'x': xdata, 
		'y1': ydata, 
		'extra1': extra_serie1
	}
	charttype = "discreteBarChart"
	data = {
			'charttype7': charttype,
			'chartdata7': chartdata,
			'chartcontainer7': "duration_hist_container"
		} 
	return data

def frequency_bin(time):
	xdata = ["1", "2", "3", "4", "5", "6+"]
	ydata = [0, 0, 0, 0, 0, 0]
	visits = time.visit_set.all()
	attendance = [v.patron.mac_addr for v in visits]
	for customer in attendance:
		if attendance.count(customer)==1:
			ydata[0]+= 1
		elif attendance.count(customer)==2:
			ydata[1]+=1
		elif attendance.count(customer)==3:
			ydata[2]+=1
		elif attendance.count(customer)==4:
			ydata[3]+=1
		elif attendance.count(customer)==5:
			ydata[4]+=1
		elif attendance.count(customer)>=6:
			ydata[5]+=1
	extra_serie1 = {"tooltip": {"y_start": "", "y_end": " visits"}}
	chartdata = {
		'x': xdata, 
		'y1': ydata, 
		'extra1': extra_serie1
	}
	charttype = "discreteBarChart"
	data = {
			'charttype8': charttype,
			'chartdata8': chartdata,
			'chartcontainer8': "frequency_hist_container"
		} 
	return data

@login_required
def detail(request, time_unit, object_id, levels=False):
	vendor_username = request.user.username
	outlet_list = Outlet.objects.filter(agent=vendor_username)
	focus = request.session['focus']
	if focus=="day":
		time = get_object_or_404(Day, pk=object_id)
		times_to_show = [h for h in time.hour_set.all() if h.hour>6 and h.hour<20]
		xdata = map(lambda h: str(h.hour), times_to_show)
	elif focus=="week":
		time = get_object_or_404(Week, pk=object_id)
		times_to_show = time.day_set.all()
		xdata = map(lambda h: str(h.datetime.strftime("%d %b")), times_to_show)
	else:
		time = get_object_or_404(Month, pk=object_id)
		times_to_show = time.day_set.all()
		xdata = map(lambda h: str(h.datetime.strftime("%d %b")), times_to_show)

	if time.vendor not in outlet_list:
		return HttpResponseRedirect('/dashboard')
	start = '08/24/2015' # what are these necessary for?
	end = '08/30/2015' # ###
	chartdata1 = create_graph(xdata, times_to_show, 'multiBarChart', 'multibarchart_container1', levels, graph_no=1, x_is_date=False, x_format='')
	chartdata2 = create_graph(xdata, times_to_show, 'multiBarChart', 'multibarchart_container2', graph_no=2, non_level=True, var_list=[6])
	# Pie chart data
	chartdata3 = customer_piechart(time)
	chartdata4 = duration_bin(time)
	chartdata5 = frequency_bin(time)
	data = dict(chartdata1.items() + chartdata2.items() + chartdata3.items() + chartdata4.items() + chartdata5.items() +  [('end',end), ('object', time), ('outlet_list', outlet_list)])
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
	campaign_list = Campaign.objects.filter(outlet=Outlet.objects.get(pk=request.session['shop_id']))
	data = {
		'object_list': campaign_list,
	}
	return render_to_response('dashboard/campaigns.html', data, context_instance=RequestContext(request))

def campaign_form(request):
	vendor_username = request.user.username
	outlet_list = Outlet.objects.filter(agent=vendor_username)
	if request.method=='POST':
		name = request.POST['name']
		end = request.POST['start']
		start = request.POST['end']
		category = request.POST['category']
		shop_id = request.POST['outlet']
		start_date = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
		end_date = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")
		shop=Outlet.objects.get(pk=int(shop_id))
		campaign = Campaign(outlet=shop, name=name, start=start_date, end=end_date, category=category)
		campaign.save()
		return render_to_response('dashboard/campaigns.html', context_instance=RequestContext(request))
	data = {
		'outlet_list': outlet_list,
			}
	return render_to_response('dashboard/campaign_form.html', data, context_instance=RequestContext(request))

def details(request):
	request.session['nav']="details"
	outlet_list = Outlet.objects.filter(agent=request.user.username)
	data = {
		'outlet_list': outlet_list,
		'store': outlet_list[0],
	}
	return render_to_response('dashboard/user_details.html', data, context_instance=RequestContext(request))

