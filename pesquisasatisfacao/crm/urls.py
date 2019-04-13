from django.urls import path

from . import views

urlpatterns = [
    path('atendimento/<int:pk>/novo/', views.atendimento_create, name='atendimento_create'),
    path('atendimento/<int:id>/editar/', views.atendimento_update, name='atendimento_update'),
    # path('pergunta/popular/', views.atendimento_populate, name='atendimento_populate'),
    path('atendimento/listar/', views.atendimento_list, name='atendimento_list'),
    path('atendimento/emails/', views.emails_list, name='emails_list'),

]