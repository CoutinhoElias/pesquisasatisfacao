# Generated by Django 2.1.3 on 2019-02-11 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190210_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
            ],
        ),
        migrations.AlterField(
            model_name='client',
            name='system',
            field=models.CharField(max_length=10, null=True, verbose_name='Sistema'),
        ),
        migrations.AddField(
            model_name='client',
            name='products',
            field=models.ManyToManyField(related_name='products', to='core.Product'),
        ),
    ]