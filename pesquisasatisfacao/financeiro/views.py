from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.datetime_safe import date

from pesquisasatisfacao.financeiro.forms import FinanceiroForm, PagamentoFormSet
from pesquisasatisfacao.financeiro.models import Conta


@login_required
def financeirot_list(request):
    q = request.GET.get('searchInput')
    print(request.GET)
    if q:
        contas = Conta.objects.filter(Q(pessoa__is_representative=False),
                                      Q(pessoa__name__icontains=q) |
                                      Q(pessoa__cdalterdata__icontains=q) |
                                      Q(valor__icontains=q) |
                                      Q(historico__descricao__icontains=q))
    else:
        contas = Conta.objects.filter(pessoa__is_representative=False)
    context = {'contas': contas}
    return render(request, 'financeiro_conta_list.html', context)


@login_required
def financeiro_create(request):
    # Cria variável na session
    request.session['person_id'] = 1

    if request.method == 'POST':
        form = FinanceiroForm(request.POST)

        # Retira toda validação do campo
        # form.errors.pop('user')

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            # new.user = request.user
            new.save()
            return HttpResponseRedirect('/financeiro/listar/')

        print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
        return render(request, 'financial_create.html', {'form': form})
    else:
        #                                 Caso precise preencher mais de um campo no form.
        context = {'form': FinanceiroForm(initial={'data_vencimento': date.today().strftime('%d/%m/%Y'),
                                                   'data_pagamento': date.today().strftime('%d/%m/%Y')})}

        # Exclui variável da session
        del request.session['person_id']

        return render(request, 'financial_create.html', context)


@login_required
def financeiro_update(request, id):

    conta = get_object_or_404(Conta, id=id)

    if request.method == 'POST':
        # Os formulários FinanceiroForm receberá o request.POST com os campos em branco
        form = FinanceiroForm(request.POST, instance=conta)
        formset = PagamentoFormSet(request.POST, instance=conta)

        # Valida os formulários MESTRE(FinanceiroForm) e DETALHE(PagamentoFormSet)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            return redirect('/financeiro/listar/')
    else:
        # Caso não seja POST ele trará o formulário com as informações preenchidas do parâmetro conta
        # que pegamos da URL quando passamos o request de id na entrada da função acima.

        form = FinanceiroForm(instance=conta)
        # Recupera a instancia de form e chama a função add_conta_item
        # para popular o detalhe com os dias do mês e o usuário poderá editar.
        # add_conta_item(period=conta.period, key=conta.id)

        formset = PagamentoFormSet(instance=conta)
    # Passamos os dois forms para uma variável com um nome qualquer (Neste caso usamos o nome "forms" afim de dar
    # a idéia
    # de mais de um formulário conforme abaixo:
    # Na linha context passamos também os dois contextos e
    # por fim na linha final passamos o retorno da função onde chamamos o template com o context.
    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'financial_update.html', context)
