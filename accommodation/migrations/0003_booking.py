# Generated by Django 3.2.3 on 2022-02-18 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0002_monthlyprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200)),
                ('phone_number', models.CharField(max_length=50, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('status', models.CharField(choices=[('E', 'enquiry'), ('P', 'pending'), ('A', 'accepted'), ('D', 'declined')], default='P', max_length=10)),
                ('order_id', models.CharField(max_length=50)),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='accommodation.property')),
            ],
            options={
                'db_table': 'table_booking',
            },
        ),
    ]
