# Generated by Django 2.2 on 2019-04-08 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0003_auto_20190408_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='valor_vendido',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor Vendido'),
        ),
    ]
