from django import forms
from django.forms import inlineformset_factory
from material import *

from pesquisasatisfacao.financeiro.models import Conta, Pagamento


class FinanceiroForm(forms.ModelForm):
    # valor_vendido = forms.CharField(label='Valor do Titulo', widget=forms.TextInput(), required=True)
    valor_vendido = forms.DecimalField(max_digits=8, decimal_places=2, localize=True)

    # def __init__(self, *args, **kwargs):
    #     super(FinanceiroForm, self).__init__(*args, **kwargs)
    #     self.fields['valor_vendido'].localize = True
    #     self.fields['valor_vendido'].widget.is_localized = True

    class Meta:
        model = Conta
        fields = ('pessoa',
                  'historico',
                  'data_vencimento',
                  'data_pagamento',
                  'valor_vendido',
                  'operacao',
                  'status',
                  'descricao')

        # exclude = ('user',)

    layout = Layout(
        Fieldset("Titulo Financeiro",
                 Row(Span12('pessoa')),
                 Row(Span3('valor_vendido'), Span2('data_vencimento'), Span2('data_pagamento'), Span5('historico')),
                 Row(Span2('operacao'), Span2('status'), Span8('descricao')),
                 ),)


PagamentoFormSet = inlineformset_factory(Conta, Pagamento,
                                         exclude=('id',),
                                         can_delete=True,
                                         fields=('data_pagamento', 'valor_pago'),
                                         extra=0)
