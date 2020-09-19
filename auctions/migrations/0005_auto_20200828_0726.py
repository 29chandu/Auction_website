# Generated by Django 3.0.3 on 2020-08-28 01:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200822_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5000000)]),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5000000)]),
        ),
    ]