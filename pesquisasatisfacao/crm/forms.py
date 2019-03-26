from django import forms

from material import *

from pesquisasatisfacao.core.models import SalesItem, Sales
from pesquisasatisfacao.crm.models import Atendimento


class AtendimentoForm(forms.ModelForm):
    feedback = forms.CharField(label='Parecer Anterior', widget=forms.Textarea(attrs={'readonly': 'readonly'}),
                               required=False)
    feedback_field = forms.CharField(label='Novo parecer', widget=forms.Textarea(),  required=True)

    class Meta:
        model = Atendimento
        fields = (
            'person',
            'type',
            'product',
            'priority',
            'feedback_field',
            'feedback',
            'user',
            'deadline',)
        exclude = ('person',)

    layout = Layout(
        Fieldset("Atendimento ",
                 Row(Span3('type'), Span9('product'), ),
                 Row(Span4('priority'), Span4('user'), Span4('deadline')),
                 Row(Span6('feedback_field'), Span6('feedback'), ),
                 ),
            )

    def __init__(self, pk,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        sales_id = Sales.objects.select_related().filter(client_id=pk)
        self.fields['product'].queryset = SalesItem.objects.filter(sales_id__in=sales_id)
        """
        A variavel pk acima vem da view atendimento_create(request, pk): onde envio esse valor
        no GET na linha 29
        context = {'form': AtendimentoForm(pk)}
        """

