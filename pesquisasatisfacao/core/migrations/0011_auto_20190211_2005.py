# Generated by Django 2.1.3 on 2019-02-11 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190211_1921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'verbose_name': 'Produto', 'verbose_name_plural': 'Produtos'},
        ),
        migrations.RemoveField(
            model_name='client',
            name='system',
        ),
    ]
