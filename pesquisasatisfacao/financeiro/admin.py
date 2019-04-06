from django.contrib import admin
from django.contrib.admin import TabularInline

from pesquisasatisfacao.financeiro.models import (PagamentoPago,
                                                  PagamentoRecebido,
                                                  Historico,
                                                  Conta,
                                                  ContaPagar,
                                                  ContaReceber)


# import locale
# locale.setlocale(locale.LC_ALL, '')
@admin.register(Historico)
class AdminHistorico(admin.ModelAdmin):
    # valor_total vem de models.py na classe HistoricoManager
    list_display = ('descricao', 'totais', 'pagar_valor_pago', 'receber_valor_pago')
    readonly_fields = ['totais', 'pagar_valor_pago', 'receber_valor_pago']

    # def totais(self, obj):
    #     if not obj.totais:
    #         return obj.totais
    #     else:
    #         return '%.2f' % obj.totais


@admin.register(Conta)
class AdminConta(admin.ModelAdmin):
    list_display = ('data_vencimento', 'valor', 'status', 'operacao', 'historico', 'pessoa',)
    search_fields = ('descricao',)
    # list_filter = ('data_vencimento', 'status', 'operacao', 'historico', 'pessoa',)


class InlinePagamentoPago(TabularInline):
    model = PagamentoPago


@admin.register(ContaPagar)
class AdminContaPagar(admin.ModelAdmin):
    list_display = ('data_vencimento', 'valor', 'status', 'historico', 'pessoa')
    search_fields = ('descricao',)
    # list_filter = ('data_vencimento','status','historico','pessoa',)
    exclude = ['operacao', ]
    inlines = [InlinePagamentoPago, ]
    date_hierarchy = 'data_vencimento'


class InlinePagamentoRecebido(TabularInline):
    model = PagamentoRecebido


@admin.register(ContaReceber)
class AdminContaReceber(admin.ModelAdmin):
    list_display = ('data_vencimento', 'valor', 'status', 'historico', 'pessoa')
    search_fields = ('descricao',)
    # list_filter = ('data_vencimento','status','historico','pessoa',)
    exclude = ['operacao', ]
    inlines = [InlinePagamentoRecebido, ]
    date_hierarchy = 'data_vencimento'
