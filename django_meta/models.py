from django.db import models


class ModelMeta(models.Model):
    class Meta:
        db_table = 'table_meta'

    slug = models.CharField(unique=True, max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)

    meta_tags = models.JSONField()

    og_tags = models.JSONField()
    twitter_tags = models.JSONField()

    # og_title = models.CharField(max_length=200)
    # og_description = models.TextField(max_length=1000)
    # og_url = models.CharField(max_length=200)
    # og_image = models.CharField(max_length=200)
    #
    # twitter_card = models.CharField(max_length=200)
    # twitter_title = models.CharField(max_length=200)
    # twitter_description = models.TextField(max_length=1000)
    # twitter_image = models.CharField(max_length=200)
    # twitter_url = models.CharField(max_length=200)
