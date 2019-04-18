from django.contrib import admin

from pesquisasatisfacao.crm.models import Typeofservice, Atendimento


@admin.register(Typeofservice)
class TypeofserviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user_destination')
    # search_fields = ('cdalterdata', 'name', 'city', 'last_search')
    # filter_horizontal = ('qualification',)


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('next_date',
                    'type',
                    'department',
                    'person',
                    'product',
                    'priority',
                    'contact',
                    'feedback',
                    'created_on',
                    'deadline',
                    'user',
                    'closed')
    # search_fields = ('cdalterdata', 'name', 'city', 'last_search')
