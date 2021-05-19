# Generated by Django 3.0.8 on 2021-05-19 01:11

from django.db import migrations, models
import media.helper


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=512)),
                ('file', models.FileField(upload_to=media.helper.RandomFileName('uploads'))),
                ('order', models.IntegerField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'table_media',
            },
        ),
    ]