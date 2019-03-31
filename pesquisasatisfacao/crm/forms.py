from django import forms

from material import *

from pesquisasatisfacao.core.models import SalesItem, Sales
from pesquisasatisfacao.crm.models import Atendimento


class AtendimentoForm(forms.ModelForm):
    feedback = forms.CharField(label='Parecer Anterior', widget=forms.Textarea(attrs={'readonly': 'readonly'}),
                               required=False)
    feedback_field = forms.CharField(label='Novo parecer', widget=forms.Textarea(),  required=True)
    deadline = forms.DateField(label='Próximo parecer',
                               widget=forms.DateInput(format='%d-%m-%Y',
                                                      attrs={'class': 'datetimepicker'}), required=False)

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
            'contact',
            'deadline',
            'closed',)
        exclude = ('person', 'priority',)

    layout = Layout(
        Fieldset("Atendimento ",
                 Row(Span3('type'), Span9('product'), ),
                 Row(Span3('user'), Span3('deadline'), Span3('contact'), Span3('closed'),),
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

