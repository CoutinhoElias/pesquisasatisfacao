from django import forms
from material import *

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

    layout = Layout(
        Fieldset("Atendimento",
                 Row(Span3('type'), Span9('product'), ),
                 Row(Span12('person'), ),
                 Row(Span4('priority'), Span4('user'), Span4('deadline')),
                 Row(Span6('feedback_field'), Span6('feedback'), ),
                 ),

            )
    # def save(self, commit=True):
    #   instance = super(AtendimentoForm, self).save(commit=False)
    #   feedback = Menu.objects.filter(project=self.project)

    # def save(self, *args, **kwargs):
    #     self.feedback = self.feedback + self.feedback_field.upper()
    #     super(AtendimentoForm, self).save(*args, **kwargs)
