from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from pesquisasatisfacao.core.models import Client
from pesquisasatisfacao.crm.forms import AtendimentoForm
from pesquisasatisfacao.crm.models import Atendimento


@login_required
def atendimento_create(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        print(request.POST, '<<<<<<<<<<<<<<<<<<<<<<<')
        form = AtendimentoForm(pk, request.POST)

        # Retira toda validação do campo
        # form.errors.pop('feedback')

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.person = client
            new.feedback = form.cleaned_data['feedback_field'] + '\n' + ('-' * 195) + '\n' + new.feedback
            new.save()
            #form.save_m2m()

            return HttpResponseRedirect('/atendimento/listar/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'atendimento_create.html', {'form': form})
    else:
        context = {'form': AtendimentoForm(pk),
                   'client': client}
        return render(request, 'atendimento_create.html', context)


@login_required
def atendimento_update(request, id):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro

    atendimento = get_object_or_404(Atendimento, id=id)

    if request.method == 'POST':
        pk = atendimento.person

        form = AtendimentoForm(pk, request.POST, instance=atendimento)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.person = pk
            new.feedback = form.cleaned_data['feedback_field'] + '\n' + ('-' * 195) + '\n' + new.feedback
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/atendimento/listar/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'atendimento_create.html', {'form': form})
    else:
        form = AtendimentoForm(pk=atendimento.person, instance=atendimento)
        client = get_object_or_404(Client, id=atendimento.person_id)

    context = {'form': form,
               'client': client}
    return render(request, 'atendimento_create.html', context)


@login_required
def atendimento_list(request):
    atendimentos = Atendimento.objects.filter(user_id=request.user).order_by("-priority", "id", "type")
    return render(request, 'atendimento_list.html', {'atendimentos': atendimentos})
