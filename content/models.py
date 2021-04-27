from django.db import models
from django.template.defaultfilters import slugify


class Content(models.Model):
    class Meta:
        db_table = 'table_content'

    title = models.CharField(max_length=200, default='')
    text = models.TextField(max_length=2048, blank=True, default='')
    slug = models.SlugField(max_length=64, default="")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Content, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

