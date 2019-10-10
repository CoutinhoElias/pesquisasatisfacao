from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.forms import inlineformset_factory
from material import *

from pesquisasatisfacao.accounts.models import UserInfo, Horario, WorkSchedule, WorkScheduleItem
from pesquisasatisfacao.core.models import Client


class RegistrationForm(forms.Form, UserCreationForm):
    base = forms.ModelChoiceField(queryset=Client.objects.filter(is_representative=True), required=False,
                                  label="Representante (Matriz ou Filial)", )

    class Meta:
        model = UserInfo
        fields = (
            'username',
            'nomecompleto',
            'base',
            'horario',
            'funcao',
            'ctps',
            'serie',
        )

    layout = Layout(
        Fieldset('Faça seu cadastro agora.', 'username',
                 Row('password1', 'password2')),
        Fieldset('Dados Pessoais', 'nomecompleto',
                 Row(Span12('base'),),
                 Row(Span6('funcao'), Span6('horario'),),
                 Row(Span4('ctps'), Span8('serie'), ),
                 ))


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Horario
        fields = (
            'description',
            'entrance',
            'lunch_entrance',
            'lunch_out',
            'exit',
        )

    layout = Layout(
        Fieldset('Registro de horário.', 'description',
                 Row('entrance', 'lunch_entrance', 'lunch_out', 'exit')),)


class WorkScheduleForm(forms.ModelForm):
    # autofocus
    # period = forms.CharField(label='Período', widget=forms.TextInput(attrs={'tabindex':"-1"}), required=True)
    user = forms.ModelChoiceField(label='Analista',
                                  widget=forms.Select(attrs={'class': 'browser-default #000000 black-text',
                                                             'disabled': 'disabled'}),
                                  required=True, queryset=UserInfo.objects.select_related().all())

    class Meta:
        model = WorkSchedule
        fields = ('period', 'user')
        # exclude = ('user',)

    layout = Layout(
        Fieldset("Preencha com o Período",
                 Row(Span3('period'), Span9('user')),),)


WorkScheduleItemFormSet = inlineformset_factory(WorkSchedule, WorkScheduleItem,
                                                # widgets={'week_day': forms.TextInput(attrs={'class': 'personal-font'}),
                                                #          'entrance': forms.TextInput(attrs={'class': 'personal-font'}),
                                                #          'lunch_entrance': forms.TextInput(
                                                #              attrs={'class': 'personal-font'}),
                                                #          'lunch_out': forms.TextInput(
                                                #              attrs={'class': 'personal-font'}),
                                                #          'lunch_exit': forms.TextInput(
                                                #              attrs={'class': 'personal-font'}),
                                                #          'exit': forms.TextInput(
                                                #              attrs={'class': 'personal-font'}),
                                                #          },
                                                
                                                exclude=('id',),
                                                can_delete=True,
                                                fields=('day',
                                                        'week_day',
                                                        'entrance',
                                                        'lunch_entrance',
                                                        'lunch_out',
                                                        'exit'),
                                                extra=0)
