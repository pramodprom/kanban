from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.models import User
from django.utils.timezone import now



# Public board (only display tasks)

def board(request):
    tasks = {
        "todo": Task.objects.filter(status="todo"),
        "in_progress": Task.objects.filter(status="in_progress"),
        "code_review": Task.objects.filter(status="code_review"),
        "done": Task.objects.filter(status="done"),
    }
    return render(request, "Task_app/board.html", {"tasks": tasks})


# Admin page: Add & list tasks
def task_admin(request):
    tasks = Task.objects.all().order_by("-created_at")
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_admin")
    else:
        form = TaskForm()
    return render(request, "Task_app/task_admin.html", {"form": form, "tasks": tasks})


# Edit Task
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_admin")
    else:
        form = TaskForm(instance=task)
    return render(request, "Task_app/edit_task.html", {"form": form})


# Delete Task
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("task_admin")   # name from your urls.py
    return render(request, "Task_app/delete_task.html", {"task": task})

def base(request):
    return render(request, "task_app/base.html")

def update_task_status(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        new_status = request.POST.get("status")

        try:
            task = Task.objects.get(id=task_id)
            task.status = new_status
            task.save()
            return JsonResponse({"success": True})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})




def analytics_dashboard(request):
    # Total tasks
    total_tasks = Task.objects.count()

    # Status counts
    todo_count = Task.objects.filter(status="todo").count()
    in_progress_count = Task.objects.filter(status="in_progress").count()
    review_count = Task.objects.filter(status="code_review").count()
    done_count = Task.objects.filter(status="done").count()

    # Completion rate
    completion_rate = (done_count / total_tasks * 100) if total_tasks > 0 else 0

    # Overdue tasks (if you have a deadline field)
    overdue_count = Task.objects.filter(deadline__lt=now(), status__in=["todo", "in_progress", "code_review"]).count()

    # Team members (users who created tasks or assigned_to if you have such field)
    team_members = User.objects.count()

    # Tasks by team member (if you have assigned_to field)
    tasks_by_member = {}
    if hasattr(Task, "assigned_to"):  # check if field exists
        for user in User.objects.all():
            tasks_by_member[user.username] = Task.objects.filter(assigned_to=user).count()
    else:
        # fallback (no assigned_to field) – just distribute tasks equally for demo
        tasks_by_member = {u.username: 0 for u in User.objects.all()}

    context = {
        "total_tasks": total_tasks,
        "todo_count": todo_count,
        "in_progress_count": in_progress_count,
        "review_count": review_count,
        "done_count": done_count,
        "completion_rate": round(completion_rate, 1),
        "overdue_count": overdue_count,
        "team_members": team_members,
        "tasks_by_member": tasks_by_member,
    }

    return render(request, "Task_app/analytics_dashboard.html", context)

