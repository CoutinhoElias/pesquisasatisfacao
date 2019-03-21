from django import forms

from pesquisasatisfacao.crm.models import Atendimento


class AtendimentoForm(forms.ModelForm):
    feedback = forms.CharField(label='Parecer Anterior', widget=forms.Textarea(attrs={'readonly': 'readonly'}))
    feedback_field = forms.CharField(label='Novo parecer', widget=forms.TextInput(),  required=False)

    class Meta:
        model = Atendimento
        fields = (
            'person',
            'type',
            'product',
            'priority',
            'feedback_field',
            'feedback',
            'deadline',)

    # def save(self, commit=True):
    #   instance = super(AtendimentoForm, self).save(commit=False)
    #   feedback = Menu.objects.filter(project=self.project)

    # def save(self, *args, **kwargs):
    #     self.feedback = self.feedback + self.feedback_field.upper()
    #     super(AtendimentoForm, self).save(*args, **kwargs)

