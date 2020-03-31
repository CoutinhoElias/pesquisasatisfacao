from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from pesquisasatisfacao.restaurant.forms import ConsumoForm
from pesquisasatisfacao.restaurant.models import Consumo
from pesquisasatisfacao.core.models import Product
# Create your views here.

@login_required
def consumo_create(request):
    # Cria variável na session
    # request.session['person_id'] = 1

    if request.method == 'POST':
        form = ConsumoForm(request.POST, request.user)

        # Retira toda validação do campo
        # form.errors.pop('user')

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            # new = form.save(commit=False)
            #new.user = request.user
            form.save(request.user)
            return HttpResponseRedirect('/consumo/lista/')
            # return HttpResponseRedirect('/')

        print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
        return render(request, 'financial_create.html', {'form': form})
    else:
        #                                 Caso precise preencher mais de um campo no form.
        context = {'form': ConsumoForm()}

        # Exclui variável da session
        # del request.session['person_id']

        return render(request, 'financial_create.html', context)


# consumidos = Product.objects.filter(user_id=request.user).order_by("-id")
@login_required
def consumo_list(request):
    consumidos = Product.objects.all().order_by("name")
    return render(request, 'consumo_list.html', {'consumidos': consumidos})