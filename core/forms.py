from django import forms
from .models import Tarefa


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'status']

        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'status': 'Status',
        }

        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Digite o título da tarefa'
            }),
            'descricao': forms.Textarea(attrs={
                'placeholder': 'Descreva a tarefa',
                'rows': 4
            }),
            'status': forms.Select(),
        }
