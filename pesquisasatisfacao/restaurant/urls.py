from django.urls import path, include
from material.frontend import urls as frontend_urls

from . import views

app_name = 'restaurant'

urlpatterns = [
    path('consumo/novo/', views.consumo_create, name='consumo_create'),
    path('consumo/lista/', views.consumo_list, name='consumo_list'),
    # path('consumo/<int:pk>/editar/', views.person_representative_update, name='person_representative_update'),
    # path('consumo/listar/', views.person_representative_list, name='person_representative_list'),
]