import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
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

@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Use POST"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"detail": "JSON inválido"}, status=400)

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({"detail": "Usuário ou senha inválidos"}, status=401)

    login(request, user)
    return JsonResponse({"ok": True, "username": user.username})


# ✅ API LOGOUT
@csrf_exempt
def api_logout(request):
    logout(request)
    return JsonResponse({"ok": True})


# ✅ API TAREFAS (LISTAR/CRIAR) - precisa estar logado
@csrf_exempt
@login_required
def api_tarefas(request):

    # GET: listar tarefas do usuário logado
    if request.method == "GET":
        tarefas = Tarefa.objects.filter(usuario=request.user).order_by("-id")
        data = []
        for t in tarefas:
            data.append({
                "id": t.id,
                "titulo": t.titulo,
                "descricao": t.descricao,
                "status": t.status,
                "status_texto": t.get_status_display() if hasattr(t, "get_status_display") else t.status,
            })
        return JsonResponse(data, safe=False)

    # POST: criar tarefa
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse({"detail": "JSON inválido"}, status=400)

        titulo = (data.get("titulo") or "").strip()
        descricao = data.get("descricao") or ""
        status = data.get("status") or "P"

        if not titulo:
            return JsonResponse({"detail": "Informe o título"}, status=400)

        tarefa = Tarefa.objects.create(
            usuario=request.user,
            titulo=titulo,
            descricao=descricao,
            status=status,
        )

        return JsonResponse({
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "status": tarefa.status,
            "status_texto": tarefa.get_status_display() if hasattr(tarefa, "get_status_display") else tarefa.status,
        }, status=201)

    return JsonResponse({"detail": "Método não permitido"}, status=405)