from django.urls import path

from . import views

app_name = 'financeiro'

urlpatterns = [
    path('financeiro/novo/', views.financeiro_create, name='financeiro_create'),
    path('financeiro/<int:id>/editar/', views.financeiro_update, name='financeiro_update'),
    path('financeiro/listar/', views.financeirot_list, name='financeirot_list'),
    path('financeiro/<int:pk>/list/', views.financeirot_client_list, name='financeirot_client_list'),

]