from django.contrib import admin
from pesquisasatisfacao.restaurant.models import Consumo

# Register your models here.
@admin.register(Consumo)
class ConsumoAdmin(admin.ModelAdmin):
    list_display = ('id','table', 'product', 'quantity', 'pay', 'data_pagamento', 'created_on','user')
    search_fields = ('table', 'product', 'quantity', 'data_pagamento','created_on')  