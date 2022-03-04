from django.db import models
from accommodation.models import Property
from authentication.models import CustomUser


class Booking(models.Model):
    class Meta:
        db_table = 'table_booking'

    ENQUIRY = 'E'
    PENDING = 'P'
    ACCEPTED = 'A'
    DECLINED = 'D'
    STATUS_CHOICES = (
        (ENQUIRY, 'enquiry'),
        (PENDING, 'pending'),
        (ACCEPTED, 'accepted'),
        (DECLINED, 'declined'),
    )

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, related_name='bookings')
    # guest = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='bookings')
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(null=True, max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    start = models.DateField()
    end = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    order_id = models.CharField(max_length=50)

    def __str__(self):
        return '%s ~ %s' % (self.start, self.end)
