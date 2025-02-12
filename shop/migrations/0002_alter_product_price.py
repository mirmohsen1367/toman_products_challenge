# Generated by Django 5.1.5 on 2025-01-17 14:34

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('2000')), django.core.validators.MaxValueValidator(Decimal('9999999999'))]),
        ),
    ]
