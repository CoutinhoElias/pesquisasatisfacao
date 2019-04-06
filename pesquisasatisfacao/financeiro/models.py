from django.db import models
from django.db.models import Sum
from django.urls import reverse


# class HistoricoManager(models.Manager):
#
#     # Criando meu Manager personalizado
#     def get_queryset(self):
#         queryset = super(HistoricoManager, self).get_queryset()
#
#         return queryset.extra(
#             select={
#                 '_valor_total': """select sum(valor) from financeiro_conta
#                                   where financeiro_conta.historico_id = financeiro_historico.id""",
#                 }
#             )


# import locale
# locale.setlocale(locale.LC_ALL, '')
class Historico(models.Model):

    @property
    def totais(self):
        return self.conta.filter(historico_id=self.id).aggregate(Sum('valor'))[
            'valor__sum']

    @property
    def valor_pago(self):
        return PagamentoPago.objects.select_related('conta', 'pagamentopago', 'historico').filter(
            conta__historico_id=self.id).aggregate(Sum('valor'))[
            'valor__sum']

    # Vai buscarna tabelao valor para somar e os parametros nas tebelas precedentes a ela.
    # PagamentoPago.objects.select_related().filter(conta__historico_id=2).aggregate(Sum('valor'))['valor__sum']

    class Meta:
        ordering = ('descricao',)
    descricao = models.CharField(max_length=50)

    # objects = HistoricoManager()

    # def valor_total(self):
    #     return self._valor_total or 0.0

    def __str__(self):
        return self.descricao


CONTA_OPERACAO_CHOICES = (
    ('d', 'Debito'),
    ('c', 'Credito'),
)

CONTA_STATUS_CHOICES = (
    ('a', 'Aberta'),
    ('p', 'Paga'),
)


class Conta(models.Model):
    class Meta:
        ordering = ('-data_vencimento', 'valor')

    pessoa = models.ForeignKey('core.client', on_delete=models.CASCADE)
    historico = models.ForeignKey('Historico', on_delete=models.CASCADE, related_name='conta')
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    operacao = models.CharField(
        max_length=1,
        default='d',
        choices=CONTA_OPERACAO_CHOICES,
        blank=True,
        )
    status = models.CharField(
        max_length=1,
        default='a',
        choices=CONTA_STATUS_CHOICES,
        blank=True,
        )
    descricao = models.TextField(blank=True)

    def __unicode__(self):
        data_vencto = self.data_vencimento.strftime('%d/%m/%Y')
        valor = '%0.02f' % self.valor
        return '%s - %s (%s)' % (valor, self.pessoa.nome, data_vencto)


class ContaPagar(Conta):
    def save(self, *args, **kwargs):
        self.operacao = 'd'
        super(ContaPagar, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Contas a Pagar'
        verbose_name = 'Conta a Pagar'

    def get_absolute_url(self):
        return reverse('conta_a_pagar', kwargs={'conta_id': self.id})


class ContaReceber(Conta):
    def save(self, *args, **kwargs):
        self.operacao = 'c'
        super(ContaReceber, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Contas a Receber'
        verbose_name = 'Conta a Receber'

    def get_absolute_url(self):
        return reverse('conta_a_receber', kwargs={'conta_id': self.id})


class Pagamento(models.Model):
    class Meta:
        abstract = True

    data_pagamento = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)


class PagamentoPago(Pagamento):
    conta = models.ForeignKey('ContaPagar', on_delete=models.CASCADE, related_name="pagamentopago",)



class PagamentoRecebido(Pagamento):
    conta = models.ForeignKey('ContaReceber', on_delete=models.CASCADE)
