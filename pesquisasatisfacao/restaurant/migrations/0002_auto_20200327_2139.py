# Generated by Django 2.2 on 2020-03-28 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumo',
            name='data_pagamento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
