from django.shortcuts import render_to_response
from django.template import RequestContext
from airline_reservations.models import *

######################
# Views ##############
######################
def airport_list(request):
    airports_list = Airport.objects.all()
    return render_to_response('test.html', locals())

def login(request):
    if request.POST:
        username = request.POST['user']
        password = request.POST['pword']

        # Log the user in and redirect
        if authenticate_customer(username, password):
            return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))
        else:
            return render_to_response('login.html', {'failed': True})
                                  #context_instance=RequestContext(request))

    return render_to_response('login.html', {},
                                  context_instance=RequestContext(request))

def book_flight():
    """Book the flights
    if a post is received book the f
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
    return False
