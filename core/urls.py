from django.urls import path
from .views import criar_tarefa, lista_tarefas

urlpatterns = [
    path('', lista_tarefas, name='lista_tarefas'),
    path('nova/', criar_tarefa, name='criar_tarefa'),

]
