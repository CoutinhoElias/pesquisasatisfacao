# Generated by Django 2.1.3 on 2019-02-08 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190206_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.CharField(max_length=30, null=True, verbose_name='E-Mail'),
        ),
        migrations.AddField(
            model_name='client',
            name='sistem',
            field=models.CharField(max_length=10, null=True, verbose_name='Sistema'),
        ),
    ]
