from django.conf.urls import patterns, url

urlpatterns = patterns('',
		url(r'^$', 'dashboard.views.dashboard', name="dashboard_home"),
#		url(r'^contact/', 'dashboard.views.contact', name="contact_page"),
		url(r'^event/', 'dashboard.views.event'),
		url(r'^(?P<day_id>\d+)/$', 'dashboard.views.detail'),
		url(r'^campaigns/', 'dashboard.views.campaigns'),
		url(r'^create/', 'dashboard.views.campaign_form'),
		)
