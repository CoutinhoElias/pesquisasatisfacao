from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.datetime_safe import date

from pesquisasatisfacao.core.models import Client
from pesquisasatisfacao.financeiro.forms import FinanceiroForm, PagamentoFormSet
from pesquisasatisfacao.financeiro.models import Conta


class Cel(object):
    """
    Class Helper used to store summaries
    """
    value = uval = None

    def __add__(self,val):
        if self.value:
            self.value = self.value +  val
        else:
            self.value = val
        self.uval = val
        return val

    def __str__(self):
        return self.uval

    def __unicode__(self):
        return self.uval

    @property
    def total(self):
        return self.value

    def reset(self):
        self.value = self.uval = None
        return self


# @login_required
# def financeirot_list(request):
#     q = request.GET.get('searchInput')
#     print(request.GET)
#     if q:
#         contas = Conta.objects.filter(Q(pessoa__is_representative=False),
#                                       Q(pessoa__name__icontains=q) |
#                                       Q(pessoa__cdalterdata__icontains=q) |
#                                       Q(valor_vendido__icontains=q) |
#                                       Q(historico__descricao__icontains=q)).order_by('data_vencimento')
#     else:
#         contas = Conta.objects.filter(pessoa__is_representative=False).order_by('data_vencimento')
#         # contanova = Conta.objects.values('data_vencimento').filter(pessoa__is_representative=False).aggregate(oldest_pubdate=Sum('valor_vendido'))
#         groups = Conta.objects.annotate(total_dia=Sum('valor_vendido')).order_by('data_vencimento')
#
#         contas.novo = 0
#         for conta in contas:
#             # print(conta.valor_vendido)
#             contas.novo = contas.novo + conta.valor_vendido
#         print(contas.novo)
#
#     context = {'contas': contas, 'groups': groups}
#     return render(request, 'financeiro_list.html', context)


import itertools


def financeiro_list(request):
    q = request.GET.get('searchInput')

    contas = Conta.objects.filter(pessoa__is_representative=False).order_by('data_vencimento')

    if q:
        contas = contas.filter(
            Q(pessoa__name__icontains=q)
            | Q(pessoa__cdalterdata__icontains=q)
            | Q(valor_vendido__icontains=q)
            | Q(historico__descricao__icontains=q)
        )

    contas = itertools.groupby(list(contas), lambda x: x.data_vencimento)
    contas = [(k, list(g)) for k, g in contas]

    # for data, group in contas:
    #     total = 0
    #
    #     print(f'Data: {data}')
    #     for transacao in group:
    #         print(transacao)
    #         if transacao.operacao == 'c':
    #             transacao.valor_vendido
    #         else:
    #             transacao.valor_vendido * -1
    #
    #         # print(f'Tipo: {transacao.operacao}) | Valor: {transacao.valor_vendido}')
    #         total += transacao.valor_vendido
    #     contass = transacao,  {total}
    #     print(f"Total: {total}")

    return render(request, 'financeiro_list.html', {'contas': contas})


@login_required
def financeirot_client_list(request, pk):
    client = get_object_or_404(Client, pk=pk)

    q = request.GET.get('searchInput')
    print(request.GET)
    if q:
        contas = Conta.objects.filter(Q(pessoa__is_representative=False,
                                        pessoa__id=pk),
                                      Q(valor_vendido__icontains=q, ) |
                                      Q(historico__descricao__icontains=q))
    else:
        contas = Conta.objects.filter(pessoa__is_representative=False,
                                      pessoa__id=pk)
    context = {'contas': contas,
               'client': client}
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
        form = FinanceiroForm(request.POST, instance=conta)
        formset = PagamentoFormSet(request.POST, instance=conta)

        # Valida os formulários MESTRE(FinanceiroForm) e DETALHE(PagamentoFormSet)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            if 'btn_submit_1' in request.POST:
                return redirect('/financeiro/' + str(id) + '/editar')
            else:
                return redirect('/financeiro/listar/')

    else:

        form = FinanceiroForm(instance=conta)
        formset = PagamentoFormSet(instance=conta)

    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'financial_update.html', context)
