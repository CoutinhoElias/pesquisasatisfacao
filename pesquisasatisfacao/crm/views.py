from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from pesquisasatisfacao.crm.forms import AtendimentoForm
from pesquisasatisfacao.crm.models import Atendimento


def atendimento_create(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST)

        # Retira toda validação do campo
        form.errors.pop('feedback')

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return HttpResponseRedirect('/atendimento/listar/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'atendimento_create.html', {'form': form})
    else:
        context = {'form': AtendimentoForm()}
        return render(request, 'atendimento_create.html', context)


def atendimento_update(request, pk):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro
    atendimento = get_object_or_404(Atendimento, pk=pk)

    if request.method == 'POST':
        form = AtendimentoForm(request.POST, instance=atendimento)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.feedback = form.cleaned_data['feedback_field'] + '\n' + ('-' * 195) + '\n' + new.feedback
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/atendimento/listar/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'atendimento_create.html', {'form': form})
    else:
        form = AtendimentoForm(instance=atendimento)
    context = {'form': form}
    return render(request, 'atendimento_create.html', context)


def atendimento_list(request):
    atendimentos = Atendimento.objects.all().order_by("-priority", "id", "type")
    return render(request, 'atendimento_list.html', {'atendimentos': atendimentos})
