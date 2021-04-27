from django.db import models

from media.helper import RandomFileName


class Media(models.Model):
    class Meta:
        db_table = 'table_media'

    title = models.CharField(max_length=512, blank=True)
    file = models.FileField(upload_to=RandomFileName('uploads'))
    order = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
