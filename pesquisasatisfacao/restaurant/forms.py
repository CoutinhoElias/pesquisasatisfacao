from django import forms
from django.db.models import Count, F, Value
from datetime import date
from material import *
from pesquisasatisfacao.restaurant.models import Consumo
from django.contrib.auth.models import User

class ConsumoForm(forms.ModelForm):
    #table = forms.IntegerField(required=True)
    #product = forms.IntegerField(required=True)
    #quantity = forms.IntegerField(required=True)
    data_pagamento = forms.DateField(required=False)

    class Meta:
        model = Consumo
        fields = ('table', 'product', 'quantity')

        exclude = ('data_pagamento', 'pay')

    layout = Layout(
        Fieldset("Lance o Pedido",
                 Row(Span12('table')),
                 Row(Span12('product')),
                 Row(Span12('quantity')),
                 ),)

    # Pagar a conta tem que excluir a mesa
    def save(self, user, commit=True, **kwargs):
        data = self.cleaned_data
        data.update({
            "user": user, 
            "created_on": date.today(),
            'pay': False
        })          
        quantity = data.pop("quantity")
        
        try:
            consumo = Consumo.objects.get(**data)
            consumo.quantity = F("quantity") + quantity
        except Consumo.DoesNotExist:
            data.update({"quantity": quantity})
            consumo = Consumo(**data)
        
        if commit:
            consumo.save()

        return consumo