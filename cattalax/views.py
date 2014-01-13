from django.shortcuts import render_to_response
from django.template import RequestContext, Context

def index(request):
	path = "/home/"
	return render_to_response('index.html', {'path': path,}, context_instance=RequestContext(request))
