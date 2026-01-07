from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('C', 'Concluída'),
    ]

    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    criada_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


