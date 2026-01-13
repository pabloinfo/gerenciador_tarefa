from django.urls import path
from . import views

urlpatterns = [

    path("", views.lista_tarefas, name="lista_tarefas"),
    path("nova/", views.criar_tarefa, name="criar_tarefa"),


    path("api/login/", views.api_login, name="api_login"),
    path("api/logout/", views.api_logout, name="api_logout"),
    path("api/tarefas/", views.api_tarefas, name="api_tarefas"),
]
