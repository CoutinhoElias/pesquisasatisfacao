import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from pesquisasatisfacao.core.forms import (QuestionForm,
                                           ClientForm,
                                           SearchForm,
                                           SearchItemFormSet, 
                                           RepresentativeForm, 
                                           SalesForm, 
                                           SalesItemFormSet)
from pesquisasatisfacao.core.models import (Search, 
                                            Question, 
                                            Client, 
                                            SearchItem, 
                                            Sales, 
                                            Group)
from pesquisasatisfacao.crm.models import Atendimento

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    # dataset = Atendimento.objects.filter(deadline__lte=datetime.now()).values('closed').annotate(
    #     attended_count=Count('closed', filter=Q(closed=True)),
    #     open_count=Count('closed', filter=Q(closed=False))).order_by('closed')

    moviments = Atendimento.objects.none()

    client_active_count = Client.objects.filter(is_representative=False).aggregate(Count('is_representative'))
    attended_count = Atendimento.objects.filter(deadline__lte=datetime.now(), closed=True).aggregate(Count('closed'))
    open_count = Atendimento.objects.filter(deadline__lte=datetime.now(), closed=False).aggregate(Count('closed'))
    attendance_count = Atendimento.objects.filter().aggregate(Count('closed'))

    moviments.cliente = moviments.total_cliente = client_active_count['is_representative__count']
    moviments.atendido = moviments.total_atendido = attended_count['closed__count']
    moviments.aberto = moviments.total_aberto = open_count['closed__count']
    moviments.atendimentos = moviments.total_atendimento = attendance_count['closed__count']

    

    context = {'moviments': moviments}
    return render(request, 'dashboard.html', context)


# @login_required
# def group_list(request):
#     groups = Group.objects.all()
#     print(groups)
#     return render(request, 'search_list.html', {'groups': groups})    


# ----------------------------------------------------------------------------------------------------------------------
@login_required
def person_client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.is_representative = False
            new.save()
            # form.save_m2m()

            return HttpResponseRedirect('/cliente/listar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'person_create.html', {'form': form})
    else:
        context = {'form': ClientForm()}
        return render(request, 'person_create.html', context)


@login_required
def person_representative_create(request):
    if request.method == 'POST':
        form = RepresentativeForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.is_representative = True
            new.save()
            # form.save_m2m()

            return HttpResponseRedirect('/cliente/listar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'representative_create.html', {'form': form})
    else:
        context = {'form': RepresentativeForm()}
        return render(request, 'representative_create.html', context)


@login_required
def person_representative_update(request, pk):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = RepresentativeForm(request.POST, instance=client)

        if form.is_valid():

            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            return redirect('/representacao/listar/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'person_create.html', {'form': form})
    else:
        form = RepresentativeForm(instance=client)
    context = {'form': form}
    return render(request, 'person_update.html', context)


@login_required
def person_client_update(request, pk):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():

            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            # return HttpResponseRedirect('/cliente/listar')
            return redirect('/cliente/' + str(client.pk) + '/pesquisas')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'person_create.html', {'form': form})
    else:
        form = ClientForm(instance=client)
    context = {'form': form,
               'client': client}
    return render(request, 'person_update.html', context)


@login_required
def person_client_home(request, pk):
    # Pega a chave da URL acima com (request, pk)
    client = get_object_or_404(Client, pk=pk)

    context = {
        'client': client,
    }
    # return render(request, 'person_home.html', context)
    return render(request, 'person_home.html', context)


@login_required
def person_populate(request):
    # Não podemos trabalhar com multiclasses com bulk create, temos que unificar as tabelas Person e Client.
    from pesquisasatisfacao.core import create_data

    lista = []

    for client in create_data.client_add:
        obj = Client(**client)
        lista.append(obj)
    print(lista[1])
    Client.objects.bulk_create(lista)

    return HttpResponseRedirect('/cliente/listar')


@login_required
def person_client_list(request):
    q = request.GET.get('searchInput')
    # print(request.GET)
    if q:
        clients = Client.objects.filter(Q(is_representative=False),
                                        Q(name__icontains=q) |
                                        Q(cdalterdata__icontains=q) |
                                        Q(last_search__icontains=q)
                                        )

    else:
        clients = Client.objects.filter(is_representative=False)

    page = request.GET.get('page', 1)
    paginator = Paginator(clients, 13)

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = {'clients': clients}
    return render(request, 'person_client_list.html', context)


@login_required
def person_representative_list(request):
    q = request.GET.get('searchInput')
    print(request.GET)
    if q:
        clients = Client.objects.filter(Q(is_representative=True),
                                        Q(name__icontains=q) |
                                        Q(cdalterdata__icontains=q) |
                                        Q(last_search__icontains=q)
                                        )
    else:
        clients = Client.objects.filter(is_representative=True)
    context = {'clients': clients}
    return render(request, 'person_representative_list.html', context)


@login_required
def person_client_detail(request, pk):
    # client = get_object_or_404(Client, person_id=pk)
    clients = Client.objects.select_related().filter(id=pk)
    searchs = Search.objects.select_related().filter(person_id=pk).values('id', 'search_key', 'researched', 'person')

    dataset = SearchItem.objects.select_related().filter(search__person_id=pk).values('question__level').annotate(
        true_count=Count('question__level', filter=Q(response=True)), false_count=Count('question__level',
                                                                                        filter=Q(response=False))
    ).order_by('question__level')

    categories = list()
    true_series_data = list()
    false_series_data = list()

    for entry in dataset:
        if entry['question__level'] == '0':
            qlevel = 'Dependência'
        elif entry['question__level'] == '1':
            qlevel = 'Confiança'
        elif entry['question__level'] == '2':
            qlevel = 'Compromentimento'
        else:
            qlevel = 'Preditiva'

        categories.append(qlevel)
        true_series_data.append(entry['true_count'])
        false_series_data.append(entry['false_count'])

    true_series = {
        'name': 'Resposta Sim',
        'data': true_series_data,
        'color': 'green'
    }

    false_series = {
        'name': 'Resposta Não',
        'data': false_series_data,
        'color': 'red'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Pesquisa Alterdata Todos os Períodos'},
        'xAxis': {'categories': categories},
        'series': [true_series, false_series]
    }

    dump = json.dumps(chart)

    # Cria variável na session
    request.session['person_id'] = pk

    context = {
        'clients': clients,
        'searchs': searchs,
        'chart': dump
    }

    return render(request, 'person_client_detail.html', context)

# ----------------------------------------------------------------------------------------------------------------------


@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return HttpResponseRedirect('/perguntas/listar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'question_create.html', {'form': form})
    else:
        context = {'form': QuestionForm()}
        return render(request, 'question_create.html', context)


@login_required
def question_update(request, pk):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():

            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/perguntas/listar')
            # return redirect('/pergunta/' + str(question.pk) + '/editar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'question_create.html', {'form': form})
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'question_create.html', context)


@login_required
def question_populate(request):

    from pesquisasatisfacao.core import create_data

    lista = []

    for question in create_data.question_add:
        obj = Question(**question)
        lista.append(obj)

    Question.objects.bulk_create(lista)

    return HttpResponseRedirect('/perguntas/listar')


@login_required
def question_list(request):
    questions = Question.objects.all().order_by("level", "id", "question")
    return render(request, 'question_list.html', {'questions': questions})


@login_required
def question_level_view(request):
    dataset = SearchItem.objects.values('question__level').annotate(
        true_count=Count('question__level', filter=Q(response=True)),
        false_count=Count('question__level', filter=Q(response=False))).order_by('question__level')

    categories = list()
    true_series = list()
    false_series = list()

    for entry in dataset:
        if entry['question__level'] == '0':
            qlevel = 'Dependência'
        elif entry['question__level'] == '1':
            qlevel = 'Confiança'
        elif entry['question__level'] == '2':
            qlevel = 'Compromentimento'
        else:
            qlevel = 'Preditiva'

        categories.append(qlevel)
        true_series.append(entry['true_count'])
        false_series.append(entry['false_count'])

    return render(request, 'dash.html', {
        'categories': json.dumps(categories),
        'true_series': json.dumps(true_series),
        'false_series': json.dumps(false_series)
    })


@login_required
def question_level_view2(request):
    dataset = SearchItem.objects.values('question__level').annotate(
        true_count=Count('question__level', filter=Q(response=True)),
        false_count=Count('question__level', filter=Q(response=False))).order_by('question__level')

    categories = list()
    true_series_data = list()
    false_series_data = list()

    for entry in dataset:
        if entry['question__level'] == '0':
            qlevel = 'Dependência'
        elif entry['question__level'] == '1':
            qlevel = 'Confiança'
        elif entry['question__level'] == '2':
            qlevel = 'Compromentimento'
        else:
            qlevel = 'Preditiva'

        categories.append(qlevel)
        true_series_data.append(entry['true_count'])
        false_series_data.append(entry['false_count'])

    true_series = {
        'name': 'Resposta Sim',
        'data': true_series_data,
        'color': 'green'
    }

    false_series = {
        'name': 'Resposta Não',
        'data': false_series_data,
        'color': 'red'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Pesquisa Alterdata Todos os Períodos'},
        'xAxis': {'categories': categories},
        'series': [true_series, false_series]
    }

    dump = json.dumps(chart)

    return render(request, 'dash2.html', {'chart': dump})


# ----------------------------------------------------------------------------------------------------------------------
def add_search_item(search):
    questions = Question.objects.all()

    for question in questions:
        SearchItem.objects.get_or_create(search=search, question=question, response='False')


@login_required
def seach_create(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            # form.save_m2m()

            search = Search.objects.get(id=new.id)
            add_search_item(search)

            # return HttpResponseRedirect('/pesquisa/listar')
            return HttpResponseRedirect(new.get_absolute_url())
            # return redirect(Search.get_absolute_url())
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            # person_instance = Person.objects.get(pk=request.session["person_id"])
            return render(request, 'seach_create.html', {'form': form})
    else:
        from datetime import date
        context = {'form': SearchForm(initial={'person': client.id,
                                               'search_key': date.today().strftime('%m-%Y')})}
        # # Exclui variável da session
        # del request.session['person_id']

        return render(request, 'seach_create.html', context)


@login_required
def search_list(request):
    seachs = Search.objects.all()
    return render(request, 'search_list.html', {'seachs': seachs})


@login_required
def pesquisa_create(request):
    # success_message = 'The Search was edited correctly.'
    if request.method == 'POST':
        form = SearchForm(request.POST)
        formset = SearchItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():

                receipt = form.save()
                formset.instance = receipt
                formset.save()

                return redirect('/cliente/listar/')

    else:
        form = SearchForm()

        formset = SearchItemFormSet()

    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'receipt_form.html', context)


@login_required
def pesquisa_update(request, pk):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro
    search = get_object_or_404(Search, pk=pk)
    # print(request.method)
    if request.method == 'POST':
        # Os formulários InvoiceForm receberá o request.POST com os campos em branco
        form = SearchForm(request.POST, instance=search)
        formset = SearchItemFormSet(request.POST, instance=search)

        # Valida os formulários MESTRE(InvoiceForm) e DETALHE(ItemFormSet)
        print(form.errors, formset.errors)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()

            # return redirect('/cliente/' + str(search.person.pk) + '/pesquisas')

            if 'btn_submit_1' in request.POST:
                return redirect('/cliente/listar/')
            else:
                return redirect('/cliente/' + str(search.person.pk) + '/pesquisas')
    else:
        # Caso não seja POST ele trará o formulário com as informações preenchidas do parâmetro invoice
        # que pegamos da URL quando passamos o request de pk na entrada da função acima.
        form = SearchForm(instance=search)
        formset = SearchItemFormSet(instance=search)

    # Passamos os dois forms para uma variável com um nome qualquer (Neste caso usamos o nome "forms" afim de dar
    # a idéia
    # de mais de um formulário conforme abaixo:
    # Na linha context passamos também os dois contextos e
    # por fim na linha final passamos o retorno da função onde chamamos o template com o context.
    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'receipt_form.html', context)
# ----------------------------------------------------------------------------------------------------------------------


class InvoiceFormView(SuccessMessageMixin, FormView):
    form_class = SalesForm
    template_name = 'invoice.html'
    success_url = reverse_lazy('core:invoice_add')
    success_message = 'The invoice was created correctly.'

    def get_context_data(self, **kwargs):
        context = super(InvoiceFormView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = SalesItemFormSet(self.request.POST, prefix='item')
        else:
            context['item_formset'] = SalesItemFormSet(prefix='item')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        contact_formset = context['item_formset']
        total = 0
        if contact_formset.is_valid():
            sale = form.save(commit=False)
            sale.save()

            contact_formset.instance = sale
            contact_formset.save()

            # for item_form in contact_formset.forms:
            #     item = item_form.save(commit=False)
            #     item.person = person
            #     item.save()
            #     total += item.quantity * item.unit_price
            # person.total = total
            # person.save()
            return super(InvoiceFormView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class InvoiceUpdateView(SuccessMessageMixin, UpdateView):
    model = Sales
    form_class = SalesForm
    template_name = 'invoice_edit.html'
    success_url = reverse_lazy('invoicing:invoice_list')
    success_message = 'The invoice was edited correctly.'

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        invoice = self.get_object()
        productos = invoice.item_set.all()
        if self.request.POST:
            context['formset'] = SalesItemFormSet(self.request.POST, prefix='items')
        else:
            context['formset'] = SalesItemFormSet(queryset=productos, prefix='items')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        total = 0
        if formset.is_valid():
            invoice = form.save(commit=False)

            formset.save()

            invoice.save()
            return super(InvoiceUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
