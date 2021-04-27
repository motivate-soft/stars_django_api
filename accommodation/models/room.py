from django.db import models

from accommodation.models import Property

TWIN = 'T'
SOFA = 'S'
QUEEN = 'Q'
KING = 'K'
CHAIR = 'C'
MURPHY = 'M'
Full = 'F'
SINGLE = 'P'

BED_CHOICES = (
    (TWIN, 'Twin Bed'),
    (SOFA, 'Sofa Bed'),
    (QUEEN, 'Queen Bed'),
    (KING, 'King Bed'),
    (CHAIR, 'Chair Bed'),
    (MURPHY, 'Murphy Bed'),
    (Full, 'Full Bed'),
    (SINGLE, 'Single Chair Sleeper Bed'),
)


class Room(models.Model):
    class Meta:
        db_table = 'table_room'

    name = models.CharField(max_length=100, null=True, blank=True)
    bed_type = models.CharField(max_length=10, choices=BED_CHOICES, default=TWIN, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, related_name='property_rooms')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}: ${self.bed_type}'
