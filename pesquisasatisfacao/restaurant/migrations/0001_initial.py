# Generated by Django 2.2 on 2020-03-28 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0012_auto_20191122_1035'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.PositiveIntegerField(verbose_name='Mesa')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('data_pagamento', models.DateField()),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em.')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_consumo_item', to='core.Product', verbose_name='Produto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Consumo_Usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Consumo Detalhe',
                'verbose_name_plural': 'Consumo Detalhes',
            },
        ),
    ]
