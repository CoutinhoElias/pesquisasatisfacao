# Generated by Django 2.1.3 on 2019-03-08 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190307_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='feriado',
            name='kind',
            field=models.CharField(choices=[('7', 'Feriado'), ('9', 'Compensação')], default='01-01-2019', max_length=1, verbose_name='Tipo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feriado',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descrição do Dia.'),
        ),
        migrations.AlterField(
            model_name='workscheduleitem',
            name='week_day',
            field=models.CharField(choices=[('6', 'Domingo'), ('0', 'Segunda'), ('1', 'Terça'), ('2', 'Quarta'), ('3', 'Quinta'), ('4', 'Sexta'), ('5', 'Sábado'), ('7', 'Feriado'), ('8', 'Faltou'), ('9', 'Compensação')], max_length=1, verbose_name='Dia Semana'),
        ),
    ]