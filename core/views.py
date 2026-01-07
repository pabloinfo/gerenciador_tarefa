from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tarefa
from .forms import TarefaForm


@login_required
def lista_tarefas(request):
    # Busca tarefas apenas do usuário logado
    tarefas = Tarefa.objects.filter(usuario=request.user)

    # CORREÇÃO: Adicionado o dicionário de contexto {'tarefas': tarefas}
    return render(request, 'core/lista_tarefas.html', {'tarefas': tarefas})


@login_required
def criar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user
            tarefa.save()
            return redirect('lista_tarefas')
    else:
        form = TarefaForm()

    return render(request, 'core/criar_tarefa.html', {'form': form})