from django.conf.urls import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'airline_reservations.views.home'),
    url(r'^bookflight/?$', 'airline_reservations.views.book_ticket'),
    url(r'^bookflight/(?P<flight_id>\d+)/?$', 'airline_reservations.views.book_ticket'),
    url(r'^login/?$', 'airline_reservations.views.login'),
    url(r'^logout/?$', 'airline_reservations.views.logout'),
	url(r'^ticket/?$', 'airline_reservations.views.ticket'),
	url(r'^ticket/(?P<booking_id>\d+)/?$', 'airline_reservations.views.ticket'),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
