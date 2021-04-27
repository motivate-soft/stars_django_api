from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from blog.utils import unique_slug_generator
from media.models import Media

User = get_user_model()


class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    short_description = models.TextField(max_length=255, blank=True, null=True)
    image = models.ForeignKey(Media, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', related_query_name='blog')
    slug = models.SlugField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_on = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def author_full_name(self):
        try:
            return f'{self.author.first_name} {self.author.last_name}'
        except:
            return "Name Not Set"

    class Meta:
        indexes = [models.Index(fields=['slug'])]
        ordering = ['-published_on']


@receiver(post_save, sender=Blog)
def generate_unique_slug_for_posts(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = unique_slug_generator(instance)
        instance.save()


@receiver(pre_save, sender=Blog)
def update_published_on(sender, instance, **kwargs):
    """Update The Date Of 'Published On' When The Post Gets Published"""

    if instance.id:
        old_value = Blog.objects.get(pk=instance.id).published_on
        if not old_value:
            instance.published_on = timezone.now()
