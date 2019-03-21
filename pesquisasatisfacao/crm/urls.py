from django.urls import path, include

from . import views

urlpatterns = [
    path('atendimento/novo/', views.atendimento_create, name='atendimento_create'),
    path('atendimento/<int:pk>/editar/', views.atendimento_update, name='atendimento_update'),
    # path('pergunta/popular/', views.question_populate, name='question_populate'),
    path('atendimento/listar/', views.atendimento_list, name='atendimento_list'),

]