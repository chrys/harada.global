from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from charts.models import HaradaChart, Task, Pillar

from .services import build_matrix_grid


# Color mapping for Tailwind classes
COLOR_CLASSES = {
    "blue": "bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100",
    "red": "bg-red-100 dark:bg-red-900 text-red-900 dark:text-red-100",
    "green": "bg-green-100 dark:bg-green-900 text-green-900 dark:text-green-100",
    "purple": "bg-purple-100 dark:bg-purple-900 text-purple-900 dark:text-purple-100",
    "yellow": "bg-yellow-100 dark:bg-yellow-900 text-yellow-900 dark:text-yellow-100",
    "pink": "bg-pink-100 dark:bg-pink-900 text-pink-900 dark:text-pink-100",
    "indigo": "bg-indigo-100 dark:bg-indigo-900 text-indigo-900 dark:text-indigo-100",
    "orange": "bg-orange-100 dark:bg-orange-900 text-orange-900 dark:text-orange-100",
}


@login_required
def matrix_view(request, chart_id):
    """Display the 9x9 matrix view of a chart."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)

    grid = build_matrix_grid(chart)

    return render(request, "matrix/view.html", {"chart": chart, "grid": grid})


@login_required
@require_http_methods(["GET"])
def pillar_modal(request, chart_id, pillar_id):
    """HTMX endpoint: Get pillar detail modal."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)
    pillar = get_object_or_404(Pillar, id=pillar_id, chart=chart)

    return render(
        request,
        "matrix/pillar_modal.html",
        {"pillar": pillar, "chart": chart, "color_classes": COLOR_CLASSES},
    )


@login_required
@require_http_methods(["POST"])
def pillar_update(request, chart_id, pillar_id):
    """HTMX endpoint: Update pillar details."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)
    pillar = get_object_or_404(Pillar, id=pillar_id, chart=chart)

    # Update pillar fields
    pillar.name = request.POST.get("name", pillar.name)
    pillar.color = request.POST.get("color", pillar.color)
    pillar.save()

    # Return empty response to close modal and let HTMX refresh the page
    return HttpResponse("")


@login_required
@require_http_methods(["GET"])
def task_modal(request, chart_id, task_id):
    """HTMX endpoint: Get task detail modal."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)
    task = get_object_or_404(Task, id=task_id, chart=chart)

    return render(request, "matrix/task_modal.html", {"task": task, "chart": chart})


@login_required
@require_http_methods(["POST"])
def task_update(request, chart_id, task_id):
    """HTMX endpoint: Update task details."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)
    task = get_object_or_404(Task, id=task_id, chart=chart)

    # Update task fields
    task.title = request.POST.get("title", task.title)
    task.description = request.POST.get("description", task.description)
    task.frequency = request.POST.get("frequency", task.frequency)
    task.status = request.POST.get("status", task.status)
    task.save()

    # Return updated task cell
    return render(request, "matrix/task_cell.html", {"task": task, "chart": chart})


@login_required
@require_http_methods(["GET"])
def task_create_modal(request, chart_id, pillar_id, position):
    """HTMX endpoint: Open a create-task modal for an empty task cell."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)
    pillar = get_object_or_404(Pillar, id=pillar_id, chart=chart)
    position = int(position)

    return render(
        request,
        "matrix/task_create_modal.html",
        {"chart": chart, "pillar": pillar, "position": position},
    )


@login_required
@require_http_methods(["POST"])
def task_create(request, chart_id, pillar_id, position):
    """HTMX endpoint: Create (or upsert) a task for an empty task cell."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)
    pillar = get_object_or_404(Pillar, id=pillar_id, chart=chart)
    position = int(position)

    title = request.POST.get("title", "").strip()
    description = request.POST.get("description", "").strip()
    frequency = request.POST.get("frequency", "one_time")
    status = request.POST.get("status", "todo")

    if title:
        Task.objects.update_or_create(
            pillar=pillar,
            position=position,
            defaults={
                "chart": chart,
                "title": title,
                "description": description,
                "frequency": frequency,
                "status": status,
            },
        )

    # Simple + reliable: reload page to reflect new grid contents.
    return HttpResponse("")
