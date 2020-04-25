from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum, F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

import itertools

from pesquisasatisfacao.restaurant.forms import ConsumoForm
from pesquisasatisfacao.restaurant.models import Consumo
from pesquisasatisfacao.core.models import Product


# Create your views here.

@login_required
def consumo_create(request, id):
    # Cria variável na session
    # request.session['person_id'] = 1
    id_product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ConsumoForm(request.POST, request.user)

        # Retira toda validação do campo
        # form.errors.pop('user')

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            # new = form.save(commit=False)
            new = form.save(request.user)
            # new.user = request.user
            new.product = id_product
            # new.save()
            
            # form.save(request.user)

            return HttpResponseRedirect('/consumo/lista/')
            # return HttpResponseRedirect('/')

        print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
        return render(request, 'consumo_create.html', {'form': form})
    else:        
        context = {'form': ConsumoForm(
            initial={'product': id_product.id, 'quantity': 1}
        )}

        # Exclui variável da session
        # del request.session['person_id']

        return render(request, 'consumo_create.html', context)


# consumidos = Product.objects.filter(user_id=request.user).order_by("-id")
@login_required
def consumo_list(request):
    consumidos = Product.objects.select_related().all().order_by("name")
    return render(request, 'consumo_list.html', {'consumidos': consumidos})


def table_resume(request):
    q = request.GET.get('searchInput')

    consumo = Consumo.objects.select_related().all().annotate(total=F('quantity') * F('product__unit_price')).order_by('table', 'product')

    if q:
        consumo = consumo.filter(
            Q(table=q)
        )

    consumo = itertools.groupby(list(consumo), lambda x: x.table)
    consumo = [(k, list(g)) for k, g in consumo]

    return render(request, 'table_resume.html', {'contas': consumo})
