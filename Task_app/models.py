from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("code_review", "Code Review"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.CharField(max_length=200)
    deadline = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.title
