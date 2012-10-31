from django.shortcuts import render_to_response
from airline_reservations.models import *

def airport_list(request):
    airports_list = Airport.objects.all()
    return render_to_response('test.html', locals())
