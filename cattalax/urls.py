from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from emailusernames.forms import EmailAuthenticationForm
# from django.core.urlresolvers import reverse_lazy

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'cattalax.views.home', name='home'),
    # url(r'^cattalax/', include('cattalax.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^$', RedirectView.as_view(url=reverse_lazy('homepage'))),
	url(r'^home/', 'cattalax.views.index', name="homepage"),
	url(r'^dashboard/', include('dashboard.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', 'auth.views.login', 
		{'authentication_form': EmailAuthenticationForm}, name='login'),
	url(r'^passwordreset', 'auth.views.password_reset'),
	url(r'^password_reset_done', 'auth.views.password_reset_done'),
	url(r'^password_reset_confirm', 'auth.views.password_reset_confirm'),
	url(r'^submit_contact', 'cattalax.views.contact'),
	url(r'^password/change/', 'auth.views.password_change', name='password_change'),
	url(r'^password/change/done', 'auth.views.password_change_done', name='password_change_done'),
	url(r'^logout', 'auth.views.logout'),
	url(r'^optout', 'dashboard.views.opt_out'),
	url(r'^data', 'dashboard.views.data'),
	url(r'accounts/', include('registration.backends.default.urls')),
	url(r'auth/', include('auth.urls')),

)
