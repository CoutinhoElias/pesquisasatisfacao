from django import forms
from django.forms import inlineformset_factory
from material import *

from pesquisasatisfacao.financeiro.models import Conta, Pagamento


class FinanceiroForm(forms.ModelForm):
    valor = forms.CharField(label='Valor do Titulo', widget=forms.NumberInput(), required=True)

    class Meta:
        model = Conta
        fields = ('pessoa',
                  'historico',
                  'data_vencimento',
                  'data_pagamento',
                  'valor',
                  'operacao',
                  'status',
                  'descricao')

        # exclude = ('user',)

    layout = Layout(
        Fieldset("Titulo Financeiro",
                 Row(Span12('pessoa')),
                 Row(Span3('valor'), Span2('data_vencimento'), Span2('data_pagamento'), Span5('historico')),
                 Row(Span2('operacao'), Span2('status'), Span8('descricao')),
                 ),)


PagamentoFormSet = inlineformset_factory(Conta, Pagamento,
                                         exclude=('id',),
                                         can_delete=True,
                                         fields=('data_pagamento', 'valor_pago'),
                                         extra=0)
