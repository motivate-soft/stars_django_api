from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify


class Content(models.Model):
    class Meta:
        db_table = 'table_content'

    title = models.CharField(max_length=200, default='')
    text = models.TextField(max_length=2048, blank=True, default='')
    slug = models.SlugField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Content)
def generate_unique_slug_for_posts(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = slugify(instance.title)
        instance.save()
