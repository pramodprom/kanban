from django.urls import path
from . import views

urlpatterns = [
    path("", views.board, name="board"),  # Public board view
    path("tasks/", views.task_admin, name="task_admin"),  # Admin task manager
    path("tasks/edit/<int:pk>/", views.edit_task, name="edit_task"),  # Edit task
    path("tasks/delete/<int:pk>/", views.delete_task, name="delete_task"),  # Delete task
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path("analytics/", views.analytics_dashboard, name="analytics_dashboard"),  # New dashboard route
    path("base/", views.base, name="base"),
]
