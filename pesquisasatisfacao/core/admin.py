from django.contrib import admin
# from django.contrib.admin import TabularInline
from django.contrib.admin import TabularInline

from pesquisasatisfacao.core.models import Client, Search, Question, SearchItem, Product, Sales, SalesItem


class InlineSales(TabularInline):
    model = SalesItem


class InlineSearchItem(TabularInline):
    model = SearchItem


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    # search_fields = ('products', 'client')
    inlines = [InlineSales, ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'name')
    search_fields = ('id', 'name')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'phone', 'cdalterdata')
    search_fields = ('cdalterdata', 'name', 'city', 'last_search')
    # inlines = [InlineSales, ]


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'search_key', 'person', 'researched')
    inlines = [InlineSearchItem, ]


@admin.register(SearchItem)
class SearchItemAdmin(admin.ModelAdmin):
    list_display = ['search', 'question', 'response']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'question', 'level')
    # search_fields = ('cdalterdata', 'name', 'email', 'last_search')
