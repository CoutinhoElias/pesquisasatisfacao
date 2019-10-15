import calendar
import datetime
import random

import weasyprint
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.template.loader import render_to_string, get_template
from django.views import View

from pesquisasatisfacao.accounts.forms import (RegistrationForm,
                                               ScheduleForm,
                                               WorkScheduleForm,
                                               WorkScheduleItemFormSet)
from pesquisasatisfacao.accounts.models import WorkSchedule, WorkScheduleItem, Feriado, Compensacao
from pesquisasatisfacao.utils import render_to_pdf


def random_time():
    entra = random.randint(8, 9)
    almoco = random.randint(entra + 3, 13)

    # ENTRADA NA EMPRESA
    if entra == 8:
        vl_en_hour = str(entra).zfill(2)
        vl_en_minute = str(random.randint(45, 59)).zfill(2)
    else:
        vl_en_hour = str(entra).zfill(2)
        vl_en_minute = str(random.randint(0, 14)).zfill(2)

    value_en = vl_en_hour + ':' + vl_en_minute
    # -------------------------------------------------------------------------------------

    # if almoco == 11:
    #     value_ea = str(almoco).zfill(2) + ':' + str(random.randint(45, 59)).zfill(2)
    # elif almoco != 11:
    #     value_ea = str(almoco).zfill(2) + ':' + str(random.randint(0, 14)).zfill(2)

    # ENTRADA NO ALMOÇO
    if entra == 8:
        vl_ea_hour = (entra + 3)
        vl_ea_minute = random.randint(45, 59)
    else:
        vl_ea_hour = (entra + 3)
        vl_ea_minute = random.randint(0, 14)

    value_ea = str(vl_ea_hour).zfill(2) + ':' + str(vl_ea_minute).zfill(2)

    # -------------------------------------------------------------------------------------

    # if value_ea == 11:
    #     value_va = str(almoco + 1).zfill(2) + ':' + str(random.randint(45, 59)).zfill(2)
    # elif value_ea != 12:
    #     value_va = str(almoco + 1).zfill(2) + ':' + str(random.randint(0, 14)).zfill(2)

    # VOLTA DO ALMOÇO
    if vl_ea_hour == 11:
        vl_va_hour = vl_ea_hour + 1
        vl_va_minute = random.randint(45, 59)

    elif vl_ea_hour == 12:
        vl_va_hour = vl_ea_hour + 1
        vl_va_minute = random.randint(0, 14)

    value_va = str(vl_va_hour).zfill(2) + ':' + str(vl_va_minute).zfill(2)

    # -------------------------------------------------------------------------------------
    # VOLTA PARA CASA
    if vl_va_hour == 11:
        vl_sa_hour = vl_va_hour + 7

    elif vl_va_hour == 12:
        vl_sa_hour = vl_va_hour + random.randint(5, 6)

        if vl_sa_hour == 17:
            vl_sa_minute = random.randint(45, 59)
        else:
            vl_sa_minute = random.randint(0, 10)

        # value_out = str(vl_va_hour + 4).zfill(2) + ':' + str(random.randint(0, 14)).zfill(2)
    elif vl_va_hour == 13:
        vl_sa_hour = vl_va_hour + 5
        vl_sa_minute = random.randint(0, 14)

        # value_out = str(vl_va_hour + 5).zfill(2) + ':' + str(random.randint(0, 14)).zfill(2)

    value_out = str(vl_sa_hour).zfill(2) + ':' + str(vl_sa_minute).zfill(2)
    print(value_en, ' - ', value_ea, ' - ', value_va, ' - ', value_out)

    return value_en, value_ea, value_va, value_out


# let alinhamentos = ['right', 'left', 'center'];
# let rand = alinhamentos[Math.floor(Math.random() * alinhamentos.length)];
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return redirect(settings.LOGIN_URL)
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'register.html', {'form': form})
    else:
        context = {'form': RegistrationForm()}
        return render(request, 'register.html', context)


@login_required
def schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'schedule.html', {'form': form})
    else:
        context = {'form': ScheduleForm()}
        return render(request, 'schedule.html', context)


def add_work_schedule_item(period, key, feriado_user):
    year_month = str(period)
    m, y = year_month.split('/')
    first_weekday, num_days_in_month = calendar.monthrange(int(y), int(m))
    work_schedule = get_object_or_404(WorkSchedule, pk=key)

    for day_number in range(1, num_days_in_month + 1):
        strdate = datetime.datetime(int(y), int(m), day_number)
        my_date = calendar.weekday(int(y), int(m), day_number)
        # my_date = calendar.day_name[strdate.weekday()]

        (value_en, value_ea, value_va, value_out) = random_time()

        ad = str(day_number).zfill(2) + '/' + m.zfill(2)
        sabado = Compensacao.objects.prefetch_related().filter(abbreviated_date=ad, users=feriado_user)
        feriado = Feriado.objects.prefetch_related().filter(abbreviated_date=ad)

        # Se a data cadastrada coincidir com feríados e compensação cadastrados via Admin
        # Ele preenche com 7 ou 9 e trata lá no template
        if sabado:
            for s in sabado:
                # if e.kind == '9':
                WorkScheduleItem.objects.get_or_create(day=strdate,
                                                       week_day=s.kind,
                                                       workschedule=work_schedule,
                                                       entrance=value_en,
                                                       lunch_entrance=value_ea,
                                                       lunch_out=value_va,
                                                       exit=value_out)
        elif feriado:
            for f in feriado:
                WorkScheduleItem.objects.get_or_create(day=strdate,
                                                       week_day=f.kind,
                                                       workschedule=work_schedule,)
        else:
            if my_date not in (5, 6, 7):
                WorkScheduleItem.objects.get_or_create(day=strdate,
                                                       week_day=my_date,
                                                       workschedule=work_schedule,
                                                       entrance=value_en,
                                                       lunch_entrance=value_ea,
                                                       lunch_out=value_va,
                                                       exit=value_out)
            else:
                WorkScheduleItem.objects.get_or_create(day=strdate,
                                                       week_day=my_date,
                                                       workschedule=work_schedule,
                                                       )


@login_required
def work_schedule_create(request):
    # Cria variável na session
    request.session['person_id'] = 1

    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)

        # Retira toda validação do campo
        form.errors.pop('user')

        if form.is_valid():
            try:
                work_schedule = WorkSchedule.objects.get(period=form.cleaned_data['period'], user=request.user)
                return HttpResponseRedirect('/accounts/ficha/' + str(work_schedule.id) + '/editar/')

            except WorkSchedule.DoesNotExist:
                print('<<<<==== FORM VALIDO ====>>>>')
                new = form.save(commit=False)
                new.user = request.user
                new.save()

                add_work_schedule_item(period=new.period, key=new.id, feriado_user=request.user)
                return HttpResponseRedirect('/accounts/ficha/' + str(new.id) + '/editar/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'work_schedule_create.html', {'form': form})
    else:
        from datetime import date
        context = {'form': WorkScheduleForm(initial={'user': request.user,
                                                     'period': date.today().strftime('%m/%Y')})}  # Caso precise preencher mais de um campo no form.

        # Exclui variável da session
        del request.session['person_id']

        return render(request, 'work_schedule_create.html', context)


@login_required
def work_schedule_update(request, id):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro
    work_schedule = get_object_or_404(WorkSchedule, id=id)
    # print(request.method)
    if request.method == 'POST':
        # Os formulários InvoiceForm receberá o request.POST com os campos em branco
        form = WorkScheduleForm(request.POST, instance=work_schedule)
        formset = WorkScheduleItemFormSet(request.POST, instance=work_schedule)

        # Retira toda validação do campo
        form.errors.pop('user')

        # Valida os formulários MESTRE(WorkScheduleForm) e DETALHE(WorkScheduleItemFormSet)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.user = request.user
                form.save()
                formset.save()
            return redirect('/accounts/ficha/listar/')
    else:
        # Caso não seja POST ele trará o formulário com as informações preenchidas do parâmetro invoice
        # que pegamos da URL quando passamos o request de pk na entrada da função acima.
        form = WorkScheduleForm(instance=work_schedule)
        # Recupera a instancia de form e chama a função add_work_schedule_item
        # para popular o detalhe com os dias do mês e o usuário poderá editar.
        # add_work_schedule_item(period=work_schedule.period, key=work_schedule.id)

        formset = WorkScheduleItemFormSet(instance=work_schedule)

    # Passamos os dois forms para uma variável com um nome qualquer (Neste caso usamos o nome "forms" afim de dar
    # a idéia
    # de mais de um formulário conforme abaixo:
    # Na linha context passamos também os dois contextos e
    # por fim na linha final passamos o retorno da função onde chamamos o template com o context.
    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'visita_form.html', context)


@login_required
def admin_receipt_pdf(request, id=id):
    work_schedule = WorkSchedule.objects.select_related('user__userinfo').get(id=id)
    work_schedule_itens = WorkScheduleItem.objects.select_related('workschedule').filter(workschedule_id=id)\
        .order_by('day')

    print(work_schedule_itens.query)

    context = {
        'work_schedule': work_schedule,
        'work_schedule_itens': work_schedule_itens
    }

    html = render_to_string('schedule_report.html', context)
    response = HttpResponse(content_type='recibo/pdf')
    response['Content-Disposition'] = 'filename="recibo_{}.pdf"'.format(work_schedule.id)
    weasyprint.HTML(string=html,
                    base_url=request.build_absolute_uri()).write_pdf(response,
                                                                     stylesheets=[weasyprint.CSS(settings.STATIC_ROOT +
                                                                                                 '/css/pdf.css')])
    return response


@login_required
def admin_receipt_pdf_preenchido(request, id=id):
    work_schedule = WorkSchedule.objects.select_related('user__userinfo').get(id=id)
    work_schedule_itens = WorkScheduleItem.objects.select_related('workschedule').filter(workschedule_id=id)\
        .order_by('day')

    print(work_schedule_itens.query)

    context = {
        "list_value": ["center-align", "left-align", "right-align"],
        'work_schedule': work_schedule,
        'work_schedule_itens': work_schedule_itens
    }

    html = render_to_string('schedule_report_preenchido.html', context)
    response = HttpResponse(content_type='recibo/pdf')
    response['Content-Disposition'] = 'filename="recibo_{}.pdf"'.format(work_schedule.id)
    weasyprint.HTML(string=html,
                    base_url=request.build_absolute_uri()).write_pdf(response,
                                                                     stylesheets=[weasyprint.CSS(settings.STATIC_ROOT +
                                                                                                 '/css/pdf.css')])
    return response


class GeneratePDF(View):
    def get(self, request, id):
        template = get_template('schedule_report.html')

        work_schedule = WorkSchedule.objects.get(id=id)
        work_schedule_item = WorkScheduleItem.objects.filter(workschedule_id=id)

        from django.db import connection
        print(connection.queries.work_schedule_item)

        context = {
            'work_schedule': work_schedule,
            'work_schedule_item': work_schedule_item
        }

        html = template.render(context)
        pdf = render_to_pdf('schedule_report.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % "12341231"
            content = "inline; filename='%s'" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required
def work_schedule_list(request):
    q = request.GET.get('searchInput')
    if q:
        work_schedules = WorkSchedule.objects.filter(Q(user=request.user) | Q(period__icontains=q))
    else:
        work_schedules = WorkSchedule.objects.filter(Q(user=request.user))
    context = {'work_schedules': work_schedules}
    return render(request, 'schedule_list.html', context)


def user_detail(request):
    user_detalhe = User.objects.filter(user=request.user)
    context = {'user_detail': user_detalhe}
    return render(context)
