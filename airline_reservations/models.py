from django.db import models

class Airport(models.Model):
    """An international or national airport"""
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    airport_name = models.CharField(max_length=50)
    is_international = models.BooleanField(default=True)

    def __unicode__(self):
        return "{0} Airport - {1}, {2}".format(self.airport_name, self.city, self.country)


class SeatType(models.Model):
    """Model to describe the seat type of the passenger
    For Example: Economy, Business, etc.
    """
    type = models.CharField(max_length=50)

    def __unicode__(self):
        return self.type


class AvailableFlight(models.Model):
    """An available flight from one airport to another"""
    departure_airport = models.ForeignKey(Airport)
    departure_time = models.DateTimeField()
    arrival_airport = models.ForeignKey(Airport, related_name="+")
    arrival_time = models.DateTimeField()
    is_international_flight = models.BooleanField()
    seat_type = models.ForeignKey(SeatType)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __unicode__(self):
        return "From {0} To {1}".format(self.departure_airport, self.arrival_airport)

