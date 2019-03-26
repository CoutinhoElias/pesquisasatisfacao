from django.contrib import admin

from pesquisasatisfacao.crm.models import Typeofservice, Atendimento


@admin.register(Typeofservice)
class TypeofserviceAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    # search_fields = ('cdalterdata', 'name', 'city', 'last_search')
    # filter_horizontal = ('qualification',)


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    # search_fields = ('cdalterdata', 'name', 'city', 'last_search')
