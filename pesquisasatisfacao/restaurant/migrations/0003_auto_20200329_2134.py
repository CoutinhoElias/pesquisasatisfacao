# Generated by Django 2.2 on 2020-03-30 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20191122_1035'),
        ('restaurant', '0002_auto_20200327_2139'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='consumo',
            unique_together={('table', 'product', 'created_on')},
        ),
    ]
