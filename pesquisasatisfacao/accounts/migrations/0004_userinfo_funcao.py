# Generated by Django 2.1.3 on 2019-02-27 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190226_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='funcao',
            field=models.CharField(default='ANALISTA', max_length=50, verbose_name='Função'),
            preserve_default=False,
        ),
    ]
