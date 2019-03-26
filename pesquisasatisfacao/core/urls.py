from django.urls import path, include
from material.frontend import urls as frontend_urls

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', include(frontend_urls)),

    path('representacao/novo/', views.person_representative_create, name='person_representative_create'),
    path('representacao/<int:pk>/editar/', views.person_representative_update, name='person_representative_update'),
    path('representacao/listar/', views.person_representative_list, name='person_representative_list'),


    path('cliente/novo/', views.person_client_create, name='person_client_create'),
    path('cliente/<int:pk>/editar/', views.person_client_update, name='person_client_update'),
    path('cliente/<int:pk>/home/', views.person_client_home, name='person_client_home'),
    path('cliente/popular/', views.person_populate, name='person_populate'),
    path('cliente/listar/', views.person_client_list, name='person_client_list'),
    path('cliente/<int:pk>/pesquisas/', views.person_client_detail, name='person_client_detail'),


    path('pergunta/nova/', views.question_create, name='question_create'),
    path('pergunta/<int:pk>/editar/', views.question_update, name='question_update'),
    path('pergunta/popular/', views.question_populate, name='question_populate'),
    path('perguntas/listar/', views.question_list, name='question_list'),

    path('pesquisa/nova/', views.seach_create, name='seach_create'),
    path('pesquisa/criar/', views.pesquisa_create, name='pesquisa_create'),
    path('pesquisa/<int:pk>/editar/', views.pesquisa_update, name='pesquisa_update'),
    path('pesquisa/listar/', views.search_list, name='search_list'),

    path('pesquisa/dash/', views.question_level_view, name='question_level_view'),
    path('pesquisa/dash2/', views.question_level_view2, name='question_level_view2'),
]