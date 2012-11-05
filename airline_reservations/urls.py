from django.conf.urls import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('airline_reservations.views',
    url(r'^/?$', 'home'),
    url(r'^bookflight/?$', 'book_ticket'),
    url(r'^bookflight/(?P<flight_id>\d+)/?$', 'book_ticket'),
    url(r'^login/?$', 'login'),
    url(r'^logout/?$', 'logout'),
	url(r'^ticket/(?P<booking_id>\d+)/?$', 'ticket'),
	url(r'^register/?$', 'registerUser'),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
