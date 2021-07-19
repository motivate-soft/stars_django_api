from django.db import models

from media.models import Media


class Company(models.Model):
    class Meta:
        db_table = 'table_company'

    name = models.CharField(max_length=200, default='')
    image = models.ForeignKey(Media, blank=True, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
