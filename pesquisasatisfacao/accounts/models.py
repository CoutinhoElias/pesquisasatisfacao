from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class UserInfo(User):
    nomecompleto = models.CharField('Nome Completo', max_length=100, null=False, blank=False)
    base = models.ForeignKey('core.client', null=True, blank=True, related_name="base",
                             on_delete=models.CASCADE, verbose_name="Base ou Representação")
    horario = models.ForeignKey('accounts.horario', null=True, blank=True, related_name="horario",
                                on_delete=models.CASCADE, verbose_name="Escolha seu Horário")

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfil de Usuários'

    def __str__(self):
        return self.nomecompleto


class Horario(models.Model):
    description = models.CharField('Descrição do Horário', max_length=100, null=False, blank=False)
    entrance = models.TimeField('Entrada', max_length=5, null=False, blank=False)
    lunch_entrance = models.TimeField('Saída almoço', max_length=5, null=False, blank=False)
    lunch_out = models.TimeField('Volta almoço', max_length=5, null=False, blank=False)
    exit = models.TimeField('Saída', max_length=5, null=False, blank=False)

    class Meta:
        verbose_name = 'Horário de Usuário'
        verbose_name_plural = 'Horário de Usuários'

    def __str__(self):
        return self.descricao


class WorkSchedule(models.Model):
    period = models.CharField(
        'Período', max_length=7, db_index=False)
    user = models.ForeignKey(
        User, related_name='Usuário', on_delete=models.CASCADE)
    created_on = models.DateTimeField(
        'Solicitado em',
        auto_now_add=True,
        auto_now=False
    )

    class Meta:
        verbose_name = 'Ficha de Visita'
        verbose_name_plural = 'Fichas de Visita'
        unique_together = (('period', 'user'),)
        ordering = ('created_on',)

    def get_absolute_url(self):
        return reverse('accounts:work_schedule_update', args=[str(self.pk)])

    def __str__(self):
        return self.period


class WorkScheduleItem(models.Model):
    workschedule = models.ForeignKey("accounts.workschedule", null=False, blank=False, related_name="children",
                                     on_delete=models.CASCADE,
                                     verbose_name="Ficha")
    day = models.DateField('Dt. Agenda', )
    entrance = models.TimeField('Entrada', max_length=5, null=True, blank=True)
    lunch_entrance = models.TimeField('Saída almoço', max_length=5, null=True, blank=True)
    lunch_out = models.TimeField('Volta almoço', max_length=5, null=True, blank=True)
    exit = models.TimeField('Saída', max_length=5, null=True, blank=True)

    class Meta:
        verbose_name = 'Ficha de Visita Detalhe'
        verbose_name_plural = 'Fichas de Visita Detalhe'

    def __str__(self):
        return self.workschedule.period
