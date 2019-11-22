# Generated by Django 2.2 on 2019-11-22 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_salesitem_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesitem',
            name='product',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='product_sale_item', to='core.Product', verbose_name='Produto'),
        ),
    ]
