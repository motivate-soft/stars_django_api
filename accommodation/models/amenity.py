from django.template.defaultfilters import slugify
from django.db import models
from media.models import Media


class Amenity(models.Model):
    class Meta:
        db_table = 'table_amenity'
        verbose_name_plural = "amenities"

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=64, default="")
    image = models.ForeignKey(Media, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Amenity, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
