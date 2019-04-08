from django.db import models
from django.db.models import Sum

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
        return Conta.objects.filter(historico_id=self.id).aggregate(Sum('valor_vendido'))[
            'valor_vendido__sum']

    def baixado(self):
        return Pagamento.objects.select_related('conta', 'historico').filter(
            conta__historico_id=self.id).aggregate(Sum('valor_pago'))[
            'valor_pago__sum']

    def restam(self):
        return (self.totais() or 0) - (self.baixado() or 0)

    # Vai buscarna tabela o valor para somar e os parametros nas tebelas precedentes a ela.
    # PagamentoPago.objects.select_related().filter(conta__historico_id=2).aggregate(Sum('valor'))['valor__sum']

    class Meta:
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao or 0


class Conta(models.Model):
    class Meta:
        ordering = ('-data_vencimento', 'valor_vendido')

    pessoa = models.ForeignKey('core.client', on_delete=models.CASCADE, related_name='client_conta')
    historico = models.ForeignKey('Historico', on_delete=models.CASCADE, related_name='historico_conta')
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    valor_vendido = models.DecimalField(max_digits=15, decimal_places=2)
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
        return self.pessoa.name


class Pagamento(models.Model):
    conta = models.ForeignKey('Conta', on_delete=models.CASCADE, related_name='conta_pagamento')
    data_pagamento = models.DateField()
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'Venda Detalhe'
        verbose_name_plural = 'Vendas Detalhe'

    def __str__(self):
        return self.conta.pessoa
