import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.datetime_safe import date

from pesquisasatisfacao.core.models import Client
from pesquisasatisfacao.crm.forms import AtendimentoForm
from pesquisasatisfacao.crm.models import Atendimento, Typeofservice

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
    username = 'myemail@gmail.com'
    password = 'mypassword'

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


def email_list_true(request):
    import email
    import imaplib

    EMAIL = 'myemail@gmail.com'
    PASSWORD = 'mypassword'
    SERVER = 'imap.gmail.com'

    # abriremos uma conexão com SSL com o servidor de emails
    # logando e navegando para a inbox
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    # selecionamos a caixa de entrada neste caso
    # mas qualquer outra caixa pode ser selecionada
    mail.select('inbox')

    # faremos uma busca com o critério ALL para pegar
    # todos os emails da inbox, esta busca retorna
    # o status da operação e uma lista com
    # os ids dos emails
    status, data = mail.search(None, 'ALL')
    # data é uma lista com ids em blocos de bytes separados
    # por espaço neste formato: [b'1 2 3', b'4 5 6']
    # então para separar os ids primeiramente criaremos
    # uma lista vazia
    mail_ids = []
    # e em seguida iteramos pelo data separando os blocos
    # de bytes e concatenando a lista resultante com nossa
    # lista inicial
    for block in data:
        # a função split chamada sem nenhum parâmetro
        # transforma texto ou bytes em listas usando como
        # ponto de divisão o espaço em branco:
        # b'1 2 3'.split() => [b'1', b'2', b'3']
        mail_ids += block.split()

    # agora para cada id baixaremos o email
    # e extrairemos seu conteúdo
    for i in mail_ids:
        # a função fetch baixa o email passando id e o formato
        # em que você deseja que a mensagem venha
        status, data = mail.fetch(i, '(RFC822)')

        # data no formato '(RFC822)' vem em uma lista com a
        # tupla onde o conteúdo está e o byte de fechamento b')'
        # por isso vamos iterar pelo data extraindo a tupla
        for response_part in data:
            # se for a tupla a extraímos o conteúdo
            if isinstance(response_part, tuple):
                # o primeiro elemento da tupla é o cabeçalho
                # de formatação e o segundo elemento possuí o
                # conteúdo que queremos extrair
                message = email.message_from_bytes(response_part[1])

                # com o resultado conseguimos pegar as
                # informações de quem enviou o email e o assunto
                mail_from = message['from']
                mail_subject = message['subject']

                # agora para o texto do email precisamos de um
                # pouco mais de trabalho pois ele pode vir em texto puro
                # ou em multipart, se for texto puro é só ir para o
                # else e extraí-lo do payload, caso contrário temos que
                # separar o que é anexo e extrair somente o texto
                if message.is_multipart():
                    mail_content = ''

                    # no caso do multipart vem junto com o email
                    # anexos e outras versões do mesmo email em
                    # diferentes formatos como texto imagem e html
                    # para isso vamos andar pelo payload do email
                    for part in message.get_payload():
                        # se o conteúdo for texto text/plain que é o
                        # texto puro nós extraímos
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

            # por fim vamos mostrar na tela o resultado da extração
            # print('<<<---------------------------------------------------------------------------->>>')
            # print({mail_from})
            # print(f'Subject: {mail_subject}')
            # print(f'Content: {mail_content}')
            # print('<<<---------------------------------------------------------------------------->>>')

            texto = mail_from
            email_ = texto.split("<")[1].split(">")[0]
            user = request.user

            add_crm_mail(email_, mail_content, mail_subject, user)

    return HttpResponseRedirect('/atendimento/listar/')
    # http://127.0.0.1:8000/atendimento/listar/


def add_crm_mail(email_, mail_content, mail_subject, user):
    typeofservice = Typeofservice.objects.get(id=1)
    user = User.objects.get(id=user.id)

    try:
        id_department, subject = mail_subject.split('-')
    except ValueError:
        id_department = 1

    print(id_department)

    try:
        client = Client.objects.get(email=email_)
        Atendimento.objects.get_or_create(type=typeofservice,
                                          department=id_department,
                                          person=client,
                                          contact=email_,
                                          feedback=mail_content,
                                          deadline=date.today(),
                                          user_id=user.id)
    except Client.DoesNotExist:
        client_default = Client.objects.get(id=1)
        Atendimento.objects.get_or_create(type=typeofservice,
                                          department='1',
                                          person=client_default,
                                          contact=email_,
                                          feedback='Este e-mail não pertence a nenhum cliente' + '\n' + mail_content,
                                          deadline=date.today(),
                                          user_id=user.id)
