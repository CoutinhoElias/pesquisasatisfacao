from django.urls import path, include

from . import views

urlpatterns = [
    path('atendimento/novo/', views.atendimento_create, name='atendimento_create'),
    path('atendimento/<int:pk>/editar/', views.atendimento_update, name='atendimento_update'),
    # path('pergunta/popular/', views.atendimento_populate, name='atendimento_populate'),
    path('atendimento/listar/', views.atendimento_list, name='atendimento_list'),

]