from django import forms
from material import *
from pesquisasatisfacao.restaurant.models import Consumo

class ConsumoForm(forms.ModelForm):
    #table = forms.IntegerField(required=True)
    #product = forms.IntegerField(required=True)
    #quantity = forms.IntegerField(required=True)
    data_pagamento = forms.DateField(required=False)

    class Meta:
        model = Consumo
        fields = ('table', 'product', 'quantity')

        exclude = ('data_pagamento',)

    layout = Layout(
        Fieldset("Lance o Pedido",
                 Row(Span12('table')),
                 Row(Span12('product')),
                 Row(Span12('quantity')),
                 ),)