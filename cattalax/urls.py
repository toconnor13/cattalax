from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
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
	url(r'^$', 'cattalax.views.index'),
	url(r'^dashboard/', include('dashboard.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', 'auth.views.login', 
		{'authentication_form': EmailAuthenticationForm}, name='login'),
	url(r'^passwordreset', 'auth.views.password_reset'),
	url(r'^password_reset_done', 'auth.views.password_reset_done'),
	url(r'^password_reset_confirm', 'auth.views.password_reset_confirm'),
	url(r'^logout', 'auth.views.logout'),
	url(r'accounts/', include('registration.backends.default.urls')),
)
