# Generated by Django 2.1.3 on 2019-02-09 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190209_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Telefone'),
        ),
    ]
