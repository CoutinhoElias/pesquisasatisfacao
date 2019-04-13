Your error refers to part of a class you haven't included,
ClientsForm, and it has an error to do with a class called Stacked,
which you haven't shown where it is imported from. Hard to diagnose
further..

Cheers

Tom

On Thu, Jul 27, 2017 at 1:02 AM, Elias Coutinho
<coutinho.elias@gmail.com> wrote:
> Traceback (most recent call last):
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/utils/autoreload.py",
> line 226, in wrapper
>     fn(*args, **kwargs)
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/core/management/commands/runserver.py",
> line 121, in inner_run
>     self.check(display_num_errors=True)
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/core/management/base.py",
> line 374, in check
>     include_deployment_checks=include_deployment_checks,
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/core/management/base.py",
> line 361, in _run_checks
>     return checks.run_checks(**kwargs)
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/core/checks/registry.py",
> line 81, in run_checks
>     new_errors = check(app_configs=app_configs)
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/core/checks/urls.py",
> line 14, in check_url_config
>     return check_resolver(resolver)
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/core/checks/urls.py",
> line 24, in check_resolver
>     for pattern in resolver.url_patterns:
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/utils/functional.py",
> line 35, in __get__
>     res = instance.__dict__[self.name] = self.func(instance)
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/urls/resolvers.py",
> line 313, in url_patterns
>     patterns = getattr(self.urlconf_module, "urlpatterns",
> self.urlconf_module)
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/utils/functional.py",
> line 35, in __get__
>     res = instance.__dict__[self.name] = self.func(instance)
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/urls/resolvers.py",
> line 306, in urlconf_module
>     return import_module(self.urlconf_name)
>   File
> "/home/eliaspai/.pyenv/versions/3.5.0/lib/python3.5/importlib/__init__.py",
> line 126, in import_module
>     return _bootstrap._gcd_import(name[level:], package, level)
>   File "<frozen importlib._bootstrap>", line 986, in _gcd_import
>   File "<frozen importlib._bootstrap>", line 969, in _find_and_load
>   File "<frozen importlib._bootstrap>", line 958, in _find_and_load_unlocked
>   File "<frozen importlib._bootstrap>", line 673, in _load_unlocked
>   File "<frozen importlib._bootstrap_external>", line 662, in exec_module
>   File "<frozen importlib._bootstrap>", line 222, in
> _call_with_frames_removed
>   File "/home/eliaspai/dani/config/urls.py", line 20, in <module>
>     url(r'^cadastro/', include('danibraz.persons.urls',
> namespace='persons')),
>   File
> "/home/eliaspai/danibraz/.danibraz/lib/python3.5/site-packages/django/conf/urls/__init__.py",
> line 50, in include
>     urlconf_module = import_module(urlconf_module)
>   File
> "/home/eliaspai/.pyenv/versions/3.5.0/lib/python3.5/importlib/__init__.py",
> line 126, in import_module
>     return _bootstrap._gcd_import(name[level:], package, level)
>   File "<frozen importlib._bootstrap>", line 986, in _gcd_import
>   File "<frozen importlib._bootstrap>", line 969, in _find_and_load
>   File "<frozen importlib._bootstrap>", line 958, in _find_and_load_unlocked
>   File "<frozen importlib._bootstrap>", line 673, in _load_unlocked
>   File "<frozen importlib._bootstrap_external>", line 662, in exec_module
>   File "<frozen importlib._bootstrap>", line 222, in
> _call_with_frames_removed
>   File "/home/eliaspai/dani/danibraz/persons/urls.py", line 5, in <module>
>     from danibraz.persons.views import clients, employees
>   File "/home/eliaspai/dani/danibraz/persons/views.py", line 6, in <module>
>     from danibraz.persons.forms import ClientsForm, EmployeeForm
>   File "/home/eliaspai/dani/danibraz/persons/forms.py", line 31, in <module>
>     class ClientsForm(Form):
>   File "/home/eliaspai/dani/danibraz/persons/forms.py", line 52, in
> ClientsForm
>     Stacked(1, 'addresses'),
> TypeError: __init__() takes 1 positional argument but 3 were given
>
>
>
>
> Em terça-feira, 25 de julho de 2017 18:16:20 UTC-3, Tim Graham escreveu:
>>
>> Please give the exception traceback.
>>
>> On Tuesday, July 25, 2017 at 3:35:41 PM UTC-4, Elias Coutinho wrote:
>>>
>>> Hello guys!
>>>
>>> I'm trying to recreate a form with Inline using django and django-stuff.
>>> I already got it once, but this is not being easy!
>>>
>>> I want to create a form that can register a Client and its addresses, or
>>> something similar to this link here.
>>>
>>> Example 1: Adding contacts.
>>>
>>> Example 2: Adding addresses.
>>>
>>> I'm trying like this:
>>>
>>> Forms.py
>>>
>>> from django import forms
>>> from material import Layout, Row, Fieldset
>>> from .models import Client
>>>
>>>
>>> class Address(forms.Form):# TA FEITO
>>>     public_place = forms.CharField(label='Logradouro')
>>>     number = forms.CharField(label='Número')
>>>     city = forms.CharField(label='Cidade')
>>>     state = forms.CharField(label='Estado')
>>>     zipcode = forms.CharField(label='Cep')
>>>     country = forms.CharField(label='País')
>>>     phone = forms.CharField(label='Fone')
>>>
>>>     class Meta:
>>>         verbose_name_plural = 'endereços'
>>>         verbose_name = 'endereço'
>>>
>>>
>>>     def __str__(self):
>>>         return self.profissao
>>>
>>>
>>> class ClientModelForm(forms.ModelForm):
>>>     class Meta:
>>>         model = Client
>>>         fields = '__all__'
>>>
>>>     layout = Layout(
>>>         Fieldset("Client",
>>>                  Row('name', ),
>>>                  Row('birthday','purchase_limit'),
>>>                  Row('address1', ),
>>>                  Row('compra_sempre', ),
>>>                  ),
>>>     )
>>>
>>>
>>>
>>> views.py
>>>
>>> import extra_views
>>> from braces.views import LoginRequiredMixin
>>> from extra_views import CreateWithInlinesView, NamedFormsetsMixin
>>> from material import LayoutMixin, Fieldset
>>> from material.admin.base import Inline
>>>
>>> from danibraz.persons.forms import *
>>> from .models import Address
>>>
>>>
>>> class ItemInline(extra_views.InlineFormSet):
>>>     model = Address
>>>     fields = ['kynd',
>>> 'public_place','number','city','state','zipcode','country','phone']#campos
>>> do endereço
>>>     extra = 1# Define aquantidade de linhas a apresentar.
>>>
>>>
>>> class NewClientsView(LoginRequiredMixin,LayoutMixin,
>>>                      NamedFormsetsMixin,
>>>                      CreateWithInlinesView):
>>>     title = "Inclua um cliente"
>>>     model = Client
>>>
>>>     #print('Chegou na linha 334')
>>>
>>>     layout = Layout(
>>>         Fieldset("Inclua um cliente",
>>>                  Row('name', ),
>>>                  Row('birthday','purchase_limit'),
>>>                  Row('address1', ),
>>>                  Row('compra_sempre', ),
>>>                  ),
>>>         Inline('Endereços', ItemInline),
>>>     )
>>>     #print('Chegou na linha 340')
>>>
>>>     def forms_valid(self, form, inlines):
>>>         new = form.save(commit=False)
>>>         new.save()
>>>         form.save_m2m()
>>>         return super(NewClientsView, self).forms_valid(form, inlines)
>>>
>>>     def get_success_url(self):
>>>         return self.object.get_absolute_url()
>>>
>>>
>>>
>>> models.py
>>>
>>> # from django.contrib.auth.models import User
>>> from django.db import models
>>>
>>>
>>> class Person(models.Model):
>>>     # class Meta:
>>>     #     abstract = True
>>>
>>>     name = models.CharField('Nome',max_length=100)
>>>     birthday = models.DateField('Aniversário')
>>>     address1 = models.CharField('Endereço 1',max_length=100)
>>>     purchase_limit = models.DecimalField('Limite de
>>> compra',max_digits=15, decimal_places=2)
>>>
>>>
>>>     class Meta:
>>>         verbose_name_plural = 'pessoas'
>>>         verbose_name = 'pessoa'
>>>
>>>     def __str__(self):
>>>         return self.name
>>>
>>>     def get_child(self):
>>>         if hasattr(self, 'client'):
>>>             return self.client
>>>         elif hasattr(self, 'employee'):
>>>             return self.employee
>>>         else:
>>>             return None
>>>
>>> def get_type(self):
>>>     if hasattr(self, 'client'):
>>>         return 'client'
>>>     elif hasattr(self, 'employee'):
>>>         return 'employee'
>>>     else:
>>>         return None
>>>
>>>
>>> class Address(models.Model):
>>>     KINDS_CHOICES = (
>>>         ('P', 'PRINCIPAL'),
>>>         ('C', 'COBRANÇA'),
>>>         ('E', 'ENTREGA'),
>>>     )
>>>
>>> person = models.ForeignKey('Person')
>>> kynd = models.CharField('Tipo', max_length=1, choices=KINDS_CHOICES)
>>> public_place = models.CharField('Logradouro',max_length=150)
>>> number = models.CharField('Número',max_length=150)
>>> city = models.CharField('Cidade',max_length=150)
>>> state = models.CharField('Estado',max_length=150)
>>> zipcode = models.CharField('Cep',max_length=10)
>>> country = models.CharField('País',max_length=150,
>>> choices=COUNTRY_CHOICES)
>>> phone = models.CharField('Fone',max_length=50)
>>>
>>> class Meta:
>>>     verbose_name_plural = 'endereços'
>>>     verbose_name = 'endereço'
>>>
>>> def __str__(self):
>>>     return self.public_place
>>>
>>>
>>>
>>> class Client(Person):
>>>     compra_sempre = models.BooleanField('Compra Sempre',default=False)
>>>
>>>         def save(self, *args, **kwargs):
>>>         super(Client, self).save(*args, **kwargs)
>>>
>>>     class Meta:
>>>         verbose_name = 'Cliente'
>>>         verbose_name_plural = 'Clientes'
>>>
>>>
>>>
>>> class Employee(Person):
>>>     ctps = models.CharField('Carteira de Trabalho',max_length=25)
>>>     salary = models.DecimalField('Salário',max_digits=15,
>>> decimal_places=2)
>>>
>>>
>>>     def save(self, *args, **kwargs):
>>>         # self.operacao = CONTA_OPERACAO_DEBITO
>>>         super(Employee, self).save(*args, **kwargs)
>>>
>>>     class Meta:
>>>         verbose_name = 'Funcionário'
>>>         verbose_name_plural = 'Funcionários'
>>>
>>>
>>>
>>> But django always returns the error quoted in the title of the post
>>>
>>> Believe me, I was able to simulate this in another project, and this one
>>> I can not replicate.
>>>
>>> This is the link that works: https://github.com/CoutinhoElias/sosmypc
>>>
>>> The URL is http://127.0.0.1:8000/site/profissoes/
>>>
>>> And this is my project that I can not replicate:
>>> Https://github.com/CoutinhoElias/danibraz
>>>
>>> All I want is something similar to the link below:
>>> http://demo.viewflow.io/materialforms/pro/signup/#python
>>> My frustration is that I got involved in a project, but I can not do it
>>> now in the danibraz!
>>> I do not know what I did differently!
>>>
> --
> You received this message because you are subscribed to the Google Groups
> "Django users" group.
> To unsubscribe from this group and stop receiving emails from it, send an
> email to django-users+unsubscribe@googlegroups.com.
> To post to this group, send email to django-users@googlegroups.com.
> Visit this group at https://groups.google.com/group/django-users.
> To view this discussion on the web visit
> https://groups.google.com/d/msgid/django-users/88e4fc9e-deb4-4e17-babc-1c51643ef31e%40googlegroups.com.
>
> For more options, visit https://groups.google.com/d/optout.

-- 
You received this message because you are subscribed to a topic in the Google Groups "Django users" group.
To unsubscribe from this topic, visit https://groups.google.com/d/topic/django-users/XFv2fYoKaE4/unsubscribe.
To unsubscribe from this group and all its topics, send an email to django-users+unsubscribe@googlegroups.com.
To post to this group, send email to django-users@googlegroups.com.
Visit this group at https://groups.google.com/group/django-users.
To view this discussion on the web visit https://groups.google.com/d/msgid/django-users/CAFHbX1JDiY9i3qpjze%3DwYcjXC%2BZ%2BWs2gU_t3FaeqO74H55F_Kw%40mail.gmail.com.
For more options, visit https://groups.google.com/d/optout.
