from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.core.mail.message import EmailMessage
from dashboard.models import Outlet

def index(request):
	outlet_list = []
	if request.user.is_authenticated:
		outlet_list=Outlet.objects.filter(agent=request.user.username)
	path = "/home/"
	return render_to_response('index.html', {'path': path, 'outlet_list': outlet_list,}, context_instance=RequestContext(request))

def contact(request):
	if request.method=='POST':
		name= request.POST['name']
		email= request.POST['email']
		company= request.POST['company']
		number= request.POST['number']
		details = name + ", " + email + ", " + company + ", " + number
		msg=EmailMessage('Web contact Form', details, 'plazasight@gmail.com', ['info@plazasight.com'])
		msg.send()
		message = "Your details have been submitted.  A response should be issued within 24 hours."
	else:
		message = "No contact details have been submitted. Please resubmit the form."
	return render_to_response('index.html', {'message': message,}, context_instance=RequestContext(request))
