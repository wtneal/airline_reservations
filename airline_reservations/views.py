from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from airline_reservations.models import *

######################
# Views ##############
######################
def airport_list(request):
    airports_list = Airport.objects.all()
    return render_to_response('test.html', locals())

def home(request):
    available_domestic_flights = get_available_flights(is_international=False)
    available_international_flights = get_available_flights(is_international=True)

    # Check the login
    if request.POST and request.POST['user'] and request.POST['pword']:
        username = request.POST['user']
        password = request.POST['pword']

        # Log the user in and redirect
        customer = authenticate_customer(username, password)
        if customer:
            # Set the session details
            request.session['user'] = customer
            return HttpResponseRedirect(reverse('airline_reservations.views.home'))
        else:
            failed = True
            return render_to_response('home.html', locals(),
                                       context_instance=RequestContext(request))

    return render_to_response('home.html', locals(),
                               context_instance=RequestContext(request))

def ticket(request):
	#customer_name = Customer.user_name //
	#return render_to_response('ticket.html', locals())

	#customer_email = Customer.email
	#return render_to_response('ticket.html', locals())
    pass


def book_ticket(request):
    """handle the ticket booking page
    the user must be logged in to access this page if they aren't send them to a login page
    """
    pass

######################
# Helper Functions ###
######################
def authenticate_customer(username, password):
    """Checks that the provided credentials match
    if the provided credentials match log the user in. return true
    otherwise return false
    """
    customer = Customer.objects.filter(username=username, password=password)
    if len(customer) == 1:
        return customer[0]
    return None

def book_flight():
    """Book the flights
    if a post is received book the flight
    """
    pass

def get_available_flights(is_international):
    return AvailableFlight.objects.filter(is_international_flight=is_international)
