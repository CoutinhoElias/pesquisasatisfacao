from django.db import models
from django.db.models import Sum, Count

CONTA_OPERACAO_CHOICES = (
    ('d', 'Debito'),
    ('c', 'Credito'),
)

CONTA_STATUS_CHOICES = (
    ('a', 'Aberta'),
    ('p', 'Paga'),
)


class Historico(models.Model):
    descricao = models.CharField(max_length=50)
    operacao = models.CharField(
        max_length=1,
        default='d',
        choices=CONTA_OPERACAO_CHOICES,
        blank=True,
    )

    def totais(self):
        return Conta.objects.filter(historico_id=self.id).aggregate(Sum('valor'))[
            'valor__sum']

    def baixado(self):
        return Pagamento.objects.select_related('conta', 'historico').filter(
            conta__historico_id=self.id).aggregate(Sum('valor'))[
            'valor__sum']

    def resta(self):
        return self.totais() - self.baixado()

    # Vai buscarna tabela o valor para somar e os parametros nas tebelas precedentes a ela.
    # PagamentoPago.objects.select_related().filter(conta__historico_id=2).aggregate(Sum('valor'))['valor__sum']

    class Meta:
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao


class Conta(models.Model):
    class Meta:
        ordering = ('-data_vencimento', 'valor')

    pessoa = models.ForeignKey('core.client', on_delete=models.CASCADE, related_name='client_conta')
    historico = models.ForeignKey('Historico', on_delete=models.CASCADE, related_name='historico_conta')
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

    def __str__(self):
        data_vencto = self.data_vencimento.strftime('%d/%m/%Y')
        valor = '%0.02f' % self.valor
        return '%s - %s (%s)' % (valor, self.pessoa.name, data_vencto)


class Pagamento(models.Model):
    conta = models.ForeignKey('Conta', on_delete=models.CASCADE, related_name='conta_pagamento')
    data_pagamento = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'Venda Detalhe'
        verbose_name_plural = 'Vendas Detalhe'

    def __str__(self):
        return '%s - %s (%s)' % (self.conta, self.conta.pessoa, self.data_pagamento)
