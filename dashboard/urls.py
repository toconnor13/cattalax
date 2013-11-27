from django.conf.urls import patterns, url

urlpatterns = patterns('',
		url(r'^$', 'dashboard.views.dashboard', name="dashboard_home"),
		url(r'^numbers/$', 'dashboard.views.dashboard', {'levels': True}),
		url(r'^contact/', 'dashboard.views.contact', name="contact_page"),
		url(r'^(?P<day_id>\d+)/$', 'dashboard.views.detail'),
		url(r'^(?P<day_id>\d+)/numbers/$', 'dashboard.views.detail', {'levels': True}),

		)
