from django.db import models
from django.template.defaultfilters import slugify
from accommodation.models import Category


class Property(models.Model):
    class Meta:
        db_table = 'table_property'
        verbose_name_plural = "properties"

    bookerville_id = models.IntegerField()
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, default="", unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    address = models.CharField(max_length=512, blank=True, default='')
    description = models.TextField(max_length=None, default='')
    neighbourhood = models.TextField(max_length=None, default='')
    transit = models.TextField(max_length=None, default='')

    # geolocation
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    # price
    price = models.IntegerField()
    min_price = models.IntegerField(null=True, blank=True)
    min_month_price = models.IntegerField(null=True, blank=True)

    # sleeps
    sleeps = models.IntegerField(default=1)
    min_sleeps = models.IntegerField(default=1, null=True, blank=True)
    bedroom_count = models.IntegerField(default=1)
    bathroom_count = models.FloatField(default=1)
    shared_bathroom = models.BooleanField(default=False)
    furnished = models.BooleanField(default=True)
    rental_parking = models.BooleanField(default=True)
    pets_considered = models.BooleanField(default=True)

    cleaning_fee = models.IntegerField(blank=True, null=True)
    transactionfee_rate = models.FloatField(blank=True, null=True)
    tax_rate = models.FloatField(blank=True, null=True)
    refundable_amount = models.IntegerField(blank=True, null=True)
    tour360 = models.CharField(max_length=100, blank=True, default='', null=True)
    featured_img = models.ForeignKey(to='media.Media', max_length=100, on_delete=models.SET_NULL,
                                     related_name='featured',
                                     blank=True, null=True)
    gallery_imgs = models.ManyToManyField(to='media.Media', related_name='property_gallery', blank=True)
    amenities = models.ManyToManyField(to='accommodation.Amenity', related_name='property_amenities', blank=True)
    similar_properties = models.ManyToManyField("self", blank=True)
    is_published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_featured_img_url(self):
        return self.featured_img.file

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Property, self).save(*args, **kwargs)
