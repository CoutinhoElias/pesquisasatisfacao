# Generated by Django 2.1.3 on 2019-03-19 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_auto_20190317_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atendimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next_date', models.DateField(auto_now=True, verbose_name='Próxima data')),
                ('priority', models.PositiveIntegerField(default=0, verbose_name='Prioridade')),
                ('feedback', models.TextField(verbose_name='Parecer')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em.')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AtendimentoClient', to='core.Client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Produtos', to='core.Product')),
            ],
            options={
                'verbose_name': 'Atendimento',
                'verbose_name_plural': 'Atendimentos',
                'ordering': ('created_on',),
            },
        ),
        migrations.CreateModel(
            name='Parecer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parecer', models.TextField(verbose_name='Parecer')),
                ('atendimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Atendimento', to='crm.Atendimento')),
            ],
        ),
        migrations.CreateModel(
            name='Typeofservice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Tipo de Atendimento')),
            ],
            options={
                'verbose_name': 'Tipo de Atendimento',
                'verbose_name_plural': 'Tipos de Atendimento',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='atendimento',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TipoDeAtendimento', to='crm.Typeofservice'),
        ),
    ]
