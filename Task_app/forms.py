from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Task
        fields = ["title", "description", "status", "deadline", "assigned_to"]
