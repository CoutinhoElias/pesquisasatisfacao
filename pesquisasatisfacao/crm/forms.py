from django import forms
from django.db.models import Count
from material import *

from pesquisasatisfacao.core.models import SalesItem, Sales, Product
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
            'closed',
            'department')
        exclude = ('person', 'priority',)

    layout = Layout(
        Fieldset("Atendimento ",
                 Row(Span3('type'), Span3('department'), Span6('product'), ),
                 Row(Span3('user'), Span3('deadline'), Span3('contact'), Span3('closed'),),
                 Row(Span6('feedback_field'), Span6('feedback'), ),
                 ),
            )

    def __init__(self, pk,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        sales_id = Sales.objects.filter(client_id=pk)
        products_id = SalesItem.objects.filter(sales_id__in=sales_id).order_by('product__name').values_list('product__id', flat=True).distinct()
        products = Product.objects.filter(id__in=products_id)
        self.fields['product'].queryset = products

        # SalesItem.objects.filter(product_id__in=products_id).distinct()
        # Product.objects.filter(product_sale_item__sales__pk__in=sales_id).distinct()

        # SalesItem.objects.filter(sales_id__in=sales_id)
        # SalesItem.objects.filter(sales_id__in=sales_id).order_by('product__name').values_list('product__name', flat=True).distinct()
        """
        A variavel pk acima vem da view atendimento_create(request, pk): onde envio esse valor
        no GET na linha 29
        context = {'form': AtendimentoForm(pk)}
        """

