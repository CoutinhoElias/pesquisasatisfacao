import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.datetime_safe import date

from pesquisasatisfacao.core.models import Client
from pesquisasatisfacao.crm.forms import AtendimentoForm
from pesquisasatisfacao.crm.models import Atendimento


import email
import imaplib  # imap pop
# pip install beautifulsoup4
from bs4 import BeautifulSoup
# import os
import mimetypes


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
            ffeedback = form.cleaned_data['feedback_field'] + '\n' + ('-' * 46) + '\n' + new.feedback
            print(ffeedback)

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

            feedback_from = 'Parecer dado no dia ' + date.today().strftime('%d/%m/%Y') + '\n' + \
                            'De: ' + str(request.user)

            feedback_to = 'Para: ' + str(form.cleaned_data['user']) + '\n' + \
                          'Com o conteúdo abaixo:' + '\n' + ('-' * 93) + '\n'
            feedback_text = form.cleaned_data['feedback_field'] + '\n' + '\n' + ('*' * 60) + '\n' + new.feedback + '\n'
            feedback = feedback_from + '\n' + feedback_to + '\n' + feedback_text


            new.feedback = feedback
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


def emails_list(request):
    username = 'coutinho.elias@gmail.com'
    password = 'fndslklkjdywywjb'

    mail = imaplib.IMAP4_SSL("imap.gmail.com")  # https:/www.google.com/settings/security/lessecureapps
    mail.login(username, password)

    mail.select("inbox")

    # Create new folder in gmail
    # mail.create("Item2")

    # List folder
    # mail.list()

    result, data = mail.uid('search', None, "ALL")

    inbox_item_list = data[0].split()

    for item in inbox_item_list:
        result2, email_data = mail.uid('fetch', item, '(RFC822)')
        raw_email = email_data[0][1].decode("latin-1")
        email_message = email.message_from_string(raw_email)
        to_ = email_message['To']
        from_ = email_message['From']
        subject_ = email_message['Subject']
        date_ = email_message['date']

        counter = 1
        for part in email_message.walk():
            if part.get_content_maintype() == "multipart":
                continue
            filename = part.get_filename()

            content_type = part.get_content_type()

            if not filename:
                # ext = 'html'
                ext = mimetypes.guess_extension(content_type)
                if not ext:
                    ext = '.bin'
                filename = 'msg-part-%08d%s' % (counter, ext)
            counter += 1
        """
        Save file
        """
        save_path = os.path.join(os.getcwd(), "emails", date_, subject_)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(os.path.join(save_path, filename), 'wb') as fp:
            fp.write(part.get_payload(decode=True))

        # print(subject_)
        # Print(content_type)
        if "plain" in content_type:
            # print(part.get_payload())
            pass
        elif "html" in content_type:
            html_ = part.get_payload()
            soup = BeautifulSoup(html_, "html.parser")
            text = soup.get_text()
            # print(subject_)
            print('--------------------------------------------------------------------------------')
            print('***** ', to_, ' *****')
            print('***** ', from_, ' *****')
            print('***** ', subject_, ' *****')
            print('***** ', text, ' *****')
            print('--------------------------------------------------------------------------------')

        else:
            pass
            # print(content_type)

    return HttpResponseRedirect('/atendimento/listar/')