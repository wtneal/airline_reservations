from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from airline_reservations.models import *

######################
# Views ##############
######################
def home(request, reg = None):
    available_domestic_flights = get_available_flights(is_international=False)
    available_international_flights = get_available_flights(is_international=True)
    request.session.set_expiry(600)     # expire after 10 min of inactivity

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

def ticket(request, booking_id):
	
    ticket_info = Booking.objects.get(id = booking_id)
    return render_to_response('ticket.html', locals())
   

def login(request):
    """login page for the user"""
    request.session.set_expiry(600)     # expire after 10 min of inactivity
    # Check the login
    if request.POST and request.POST['user'] and request.POST['pword']:
        username = request.POST['user']
        password = request.POST['pword']

        # Log the user in and redirect
        customer = authenticate_customer(username, password)
        if customer:
            # Set the session details
            request.session['user'] = customer
            referer = request.session.get('referer')
            if referer:
                return HttpResponseRedirect(referer)
            else:
                return HttpResponseRedirect(reverse('airline_reservations.views.home'))
        else:
            failed = True
            return render_to_response('login.html', locals(),
                                       context_instance=RequestContext(request))

    return render_to_response('login.html', locals(),
                               context_instance=RequestContext(request))

def logout(request):
    """log the user out and redirect to the home page"""
    request.session.clear()
    return HttpResponseRedirect(reverse('airline_reservations.views.home'))


def book_ticket(request, flight_id=None):
    """handle the ticket booking page
    the user must be logged in to access this page if they aren't send them to a login page
    """
    if not request.session.get('user'):
        if flight_id:
            request.session['referer'] = reverse('airline_reservations.views.book_ticket', args=(flight_id,))
        else:
            request.session['referer'] = reverse('airline_reservations.views.book_ticket')
        return HttpResponseRedirect(reverse('airline_reservations.views.login'))

    if request.POST:
        result = book_flight(request.session.get('user'), request.POST)
        if result:
            return HttpResponseRedirect(reverse('airline_reservations.views.ticket', args=(result,)))
        else:
            failed = True

    if flight_id:
        flight = AvailableFlight.objects.get(id=flight_id)
        return render_to_response('book_flight.html', locals(),
                               context_instance=RequestContext(request))
    else:
        if request.GET:
            # Get a list of flights that match these params
            flights = get_available_flights(is_international=True, get_vars=request.GET)
            print(flights)

        airports = Airport.objects.all()
        classes = SeatType.objects.all()
        return render_to_response('find_flight.html', locals(), context_instance=RequestContext(request))

def registerUser(request):
	if request.POST:
	
		try:
			user = register(request.POST)
			#reg = 1
			request.session['user'] = user
			
			#return HttpResponseRedirect(reverse('airline_reservation.views.home', args=(reg,)))	
			
			
			#return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		except ValueError:
			failed = True
		return HttpResponseRedirect(reverse('airline_reservation.views.home'))
	return render_to_response('register.html', locals(), context_instance=RequestContext(request))

def confirm(request):
	
	
	#if request.POST:
	#	username = register(request.POST)
	#	return HttpResponseRedirect(reverse('airlines_reservation.views.home', args=(username,)))
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

def book_flight(customer, form_fields):
    """Book the flights
    returns id of the booked flight if the booking was successful
    """
    if form_fields.get('flight'):
        flight = AvailableFlight.objects.get(id=form_fields.get('flight'))
    if form_fields.get('adults'):
        adults = form_fields.get('adults')
    if form_fields.get('children'):
        children = form_fields.get('children')
    if form_fields.get('infants'):
        infants = form_fields.get('infants')
    b = Booking(customer=customer, flight=flight, adults=adults, children=children, infants=infants)
    b.save()
    return b.id

def register(form_fields):
	"""New User Registration """
	if form_fields.get('name'):
		name = form_fields.get('name')
	else:
		raise ValueError
	if form_fields.get('email'):
		email = form_fields.get('email')
	else:
		raise ValueError
	if form_fields.get('username'):
		username = form_fields.get('username')
	else:
		raise ValueError
	if form_fields.get('password'):
		password = form_fields.get('password')
	else:
		raise ValueError
	customer = Customer(name=name, email=email, username=username, password=password)
	customer.save()
	return customer

def get_available_flights(is_international, get_vars=None):
# Verify that the data is valid
    if get_vars:
        flights = AvailableFlight.objects.filter(is_international_flight=is_international)
        if get_vars.get('from'):
            flights = flights.filter(departure_airport=get_vars.get('from'))
        if get_vars.get('to'):
            flights = flights.filter(arrival_airport=get_vars.get('to'))
        # TODO date comparisions
        #if get_vars.get('booking_date'):
        #    flights = flights.filter(departure_time=get_vars.get('booking_date'))
        if get_vars.get('seat_type'):
            flights = flights.filter(seat_type=get_vars.get('seat_type'))
        return flights
    return AvailableFlight.objects.filter(is_international_flight=is_international)
