from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.core.mail.message import EmailMessage

def index(request):
	path = "/home/"
	return render_to_response('index.html', {'path': path,}, context_instance=RequestContext(request))

def contact(request):
	if request.method=='POST':
		name= request.POST['name']
		email= request.POST['email']
		company= request.POST['company']
		number= request.POST['number']
		details = name + ", " + email + ", " + company + ", " + number
		msg=EmailMessage('Web contact Form', details, 'plazasight@gmail.com', ['plazasight@gmail.com'])
		msg.send()
		message = "Your details have been submitted.  A response should be issued withing 24 hours."
	else:
		message = "No contact details have been submitted. Please resubmit the form."
	return render_to_response('index.html', {'message': message,}, context_instance=RequestContext(request))
