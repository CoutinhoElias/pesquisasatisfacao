from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Typeofservice(models.Model):
    name = models.CharField('Tipo de Atendimento', max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tipo de Atendimento'
        verbose_name_plural = 'Tipos de Atendimento'

    def __str__(self):
        return self.name


class Atendimento(models.Model):
    next_date = models.DateField(
        'Próxima data',
        auto_now_add=False,
        auto_now=True
    )
    type = models.ForeignKey('crm.typeofservice', related_name='TipoDeAtendimento', verbose_name='Tipo de atendimento',
                             on_delete=models.CASCADE)
    person = models.ForeignKey('core.client', related_name='AtendimentoClient', on_delete=models.CASCADE)
    product = models.ForeignKey('core.product', related_name='Produtos', verbose_name='Produto',
                                on_delete=models.CASCADE)
    priority = models.PositiveIntegerField('Prioridade', default=0)
    feedback = models.TextField('Parecer Anterior', null=True, blank=True)
    created_on = models.DateField(
        'Criado em.',
        auto_now_add=False,
        auto_now=True
    )
    deadline = models.DateField('Próximo Parecer')
    user = models.ForeignKey(User, verbose_name="Enviar para", on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_on',)
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'

    # @property # question__name
    # def feedback_field(self):
    #     """Returns the feedback_field null."""
    #     return '%s' % 'Digite seu parecer'

    def __str__(self):
        return self.type.name

    def get_absolute_url(self):
        return reverse('atendimento_update', args=[str(self.pk)])

#
# class Parecer(models.Model):
#     atendimento = models.ForeignKey('crm.atendimento', related_name='Atendimento', on_delete=models.CASCADE)
#     parecer = models.TextField('Parecer',)
