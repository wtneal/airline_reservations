from django.db import models

class Airport(models.Model):
    """An international or national airport"""
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    airport_name = models.CharField(max_length=50)
    is_international = models.BooleanField(default=True)

    def __unicode__(self):
        return "{1} {2}, {3}".format(self.airport_name, self.city, self.country)

class AvailableFlights(models.Model):
    """An available flight from one airport to another"""
    departure_airport = models.ForeignKey(Airport)
    departure_time = models.TimeField()
    arrival_airport = models.ForeignKey(Airport)
    arrival_time = models.TimeField()
    is_international_flight = models.BooleanField()
    seat_type = models.ForeignKey(SeatType)

class SeatType(models.Model):
    """Model to describe the seat type of the passenger
    For Example: Economy, Business, etc.
    """
    type = models.CharField(max_length=50)
