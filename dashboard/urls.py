from django.conf.urls import patterns, url

urlpatterns = patterns('',
		url(r'^$', 'dashboard.views.dashboard', name="dashboard_home"),
#		url(r'^contact/', 'dashboard.views.contact', name="contact_page"),
		url(r'^event/', 'dashboard.views.event'),
		url(r'^(?P<time_unit>\w+)/(?P<object_id>\d+)/$', 'dashboard.views.detail'),
		url(r'^campaigns/', 'dashboard.views.campaigns'),
		url(r'^add/', 'dashboard.views.campaign_form'),
		url(r'^details/', 'dashboard.views.details'),
		)
