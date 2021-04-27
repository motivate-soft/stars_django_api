from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    class Meta:
        db_table = 'table_category'
        verbose_name_plural = "categories"
    name = models.CharField(max_length=64, default='')
    slug = models.SlugField(max_length=64, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)




