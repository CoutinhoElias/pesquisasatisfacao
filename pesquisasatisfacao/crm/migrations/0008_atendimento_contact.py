# Generated by Django 2.1.3 on 2019-03-26 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20190325_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='atendimento',
            name='contact',
            field=models.TextField(blank=True, max_length=50, null=True, verbose_name='Contato'),
        ),
    ]