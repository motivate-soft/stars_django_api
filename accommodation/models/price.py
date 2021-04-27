from django.db import models
from django.utils.translation import gettext_lazy as _

from accommodation.models import Property


class Price(models.Model):
    price = models.IntegerField(_("price for specific period"), null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="pricing_items")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # end_date = models.DateField(blank=True, null=True, format="%Y-%m-%d %H:%M:%S", input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])

    class Meta:
        db_table = 'table_price'
        verbose_name = _("price")
        verbose_name_plural = _("prices")

    def __str__(self):
        return f'{self.start_date} ~ {self.end_date}: {self.price}'
