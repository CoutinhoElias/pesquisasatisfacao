from django.core.serializers import json
import json
from django.db import transaction
from django.db.models import Count, Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import TemplateView

from pesquisasatisfacao.core.forms import QuestionForm, ClientForm, PersonForm, SearchForm, SearchItemFormSet
from pesquisasatisfacao.core.models import Search, Question, Client, Person, SearchItem


def home(request):
    return render(request, 'base.html')

#-----------------------------------------------------------------------------------------------------------------------


def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return HttpResponseRedirect('/pessoa/listar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'person_create.html', {'form':form})
    else:
        context = {'form': PersonForm()}
        return render(request, 'person_create.html', context)


def person_list2(request):
    persons = Person.objects.all().order_by("cdalterdata")
    return render(request, 'person_list.html', {'persons': persons})


def person_list(request):
    q = request.GET.get('searchInput')
    print(request.GET)
    if q:
        pessoas = Person.objects.filter(name__icontains=q)
    else:
        pessoas = Person.objects.all()
    context = {'pessoas': pessoas}
    print(context)
    return render(request, 'person_list.html', context)

#-----------------------------------------------------------------------------------------------------------------------


def person_client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return HttpResponseRedirect('/cliente/listar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'person_create.html', {'form':form})
    else:
        context = {'form': ClientForm()}
        return render(request, 'person_create.html', context)


def person_client_list(request):
    clients = Client.objects.select_related('person_ptr').all().order_by("cdalterdata")
    return render(request, 'person_client_list.html', {'clients': clients})


#-----------------------------------------------------------------------------------------------------------------------


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
            return render(request, 'question_create.html', {'form':form})
    else:
        context = {'form': QuestionForm()}
        return render(request, 'question_create.html', context)


def question_list(request):
    questions = Question.objects.all().order_by("question")
    return render(request, 'question_list.html', {'questions': questions})

#-----------------------------------------------------------------------------------------------------------------------


def seach_create(request):

        if request.method == 'POST':
            form = SearchForm(request.POST)

            if form.is_valid():
                print('<<<<==== FORM VALIDO ====>>>>')
                new = form.save(commit=False)
                new.save()
                # form.save_m2m()

                return HttpResponseRedirect('/pesquisa/listar')
            else:
                print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
                # person_instance = Person.objects.get(pk=request.session["person_id"])
                return render(request, 'seach_create.html', {'form': form})
        else:
            if 'person_id' in request.session:
                # Recupera variável da session
                pessoa_id = request.session['person_id']
                from datetime import date
                context = {'form': SearchForm(initial={'person': pessoa_id,
                                                       'search_key': date.today().strftime('%m-%Y')})}
                # Caso precise preencher mais de um campo no form.
                # context = {'form': SearchForm(initial={'person': pessoa_id, 'search_key': '11-2018'})}

                # Exclui variável da session
                del request.session['person_id']

                return render(request, 'seach_create.html', context)
            else:
                # Caso person_id não exista na session ele redireciona para lista de clientes pesquisados.
                return HttpResponseRedirect('/cliente/listar')


def search_list(request):
    seachs = Search.objects.all()
    return render(request, 'search_list.html', {'seachs': seachs})

#-----------------------------------------------------------------------------------------------------------------------


def person_client_detail(request, pk):
    # client = get_object_or_404(Client, person_id=pk)
    clients = Client.objects.select_related('person_ptr').filter(person_ptr=pk)
    searchs = Search.objects.select_related('person', 'search').filter(person_id=pk).values('id', 'search_key',
                                                                                            'researched', 'person')

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
#
# def addQuestions(**data):
#     questions = Question.objects.all()
#
#     for question in questions:
#
#         try:
#             Search.objects.get(
#                 search_key=data['search_key'],
#                 person=data['person'],
#                 researched=data['researched'],
#                 question=question,
#             )
#             print('existe')
#         except Search.DoesNotExist:
#             Search.objects.get_or_create(
#                 search_key=data['search_key'],
#                 person=data['person'],
#                 researched=data['researched'],
#                 question=question
#             )
#             print('Não existe')
#
#     return HttpResponseRedirect('/')

class SearchDetailWiew(TemplateView):
    template_name = 'search.html'

    def get_formset(self, clear=False):
        QuestionsFormSet = modelformset_factory(
            Search, fields=('response',), can_delete=False, extra=0
        )
        # Soluçao alternativa
        client = Client.objects.last()
        if clear:

            formset = QuestionsFormSet(
                queryset = Search.objects.filter(search_key='11/2018', person=client)
            )
        else:
            formset = QuestionsFormSet(
                queryset = Search.objects.filter(search_key='11/2018', person=client),
                data=self.request.POST or None
            )

        return formset

    def get_context_data(self, **kwargs):
        context = super(SearchDetailWiew, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            print('Formulário válido!')
            formset.save()
            print('Dados salvos!')
            context['formset'] = self.get_formset(clear=True)
        else:
            print(formset)
        return self.render_to_response(context)


search_list2 = SearchDetailWiew.as_view()


def pesquisa_editar3(request):

    searchformfet = modelformset_factory(Search, fields='__all__', extra=0)
    if request.method == "POST":
        formset = searchformfet(request.POST)

        if formset.is_valid():
            message = "Thank you"
            for form in formset:
                print(form)
                form.save()
        else:
            message = "Something went wrong"

        return render_to_response('search2.html',
                {'message': message}, RequestContext(request))
    else:
        return render_to_response('search2.html',
                {'formset': searchformfet()}, RequestContext(request))


# def pesquisa_editar(request):
#     questionsformset = modelformset_factory(Search, fields=('person', ), extra=0)
#     novapesquisa=Search.objects.all()
#
#     if request.method == 'POST':
#         #form = QuestionsFormSet(queryset=Search.objects.all())
#         #formset = questionsformset(request.POST)
#         formset = questionsformset(request.POST)
#
#         #instances = form.save(commit=False)
#
#         #for instance in instances:
#         #   instance.save()
#
#         instances = formset.save()
#
#     form = questionsformset()
#     print(form)
#
#     context = {'form': form}
#     return render(request, 'search_funcionando.html', context)


def pesquisa_create(request):
    success_message = 'The Search was edited correctly.'
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
        # initial={'author': request.user}
        formset = SearchItemFormSet()

    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'receipt_form.html', context)


def pesquisa_update(request, pk):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro
    search = get_object_or_404(Search, pk=pk)
    print(request.method)
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

            return redirect('/cliente/listar/')
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


