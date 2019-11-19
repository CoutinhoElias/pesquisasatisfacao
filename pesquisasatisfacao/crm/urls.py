from django.urls import path

from . import views

app_name = 'crm'

urlpatterns = [
    path('atendimento/cliente/<int:pk>/novo/', views.atendimento_create, name='atendimento_create'),
    path('atendimento/<int:id>/cliente/<int:cl>/editar/', views.atendimento_update, name='atendimento_update'),
    # path('pergunta/popular/', views.atendimento_populate, name='atendimento_populate'),
    path('atendimento/listar/', views.atendimento_list, name='atendimento_list'),

    path('atendimento/emails/', views.emails_list, name='emails_list'),
    path('atendimento/emails_true/', views.email_list_true, name='emails_list_true'),
]