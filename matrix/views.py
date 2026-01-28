from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from charts.models import HaradaChart, Task


@login_required
def matrix_view(request, chart_id):
    """Display the 9x9 matrix view of a chart."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)

    # Build 9x9 grid data
    grid = build_matrix_grid(chart)

    return render(request, "matrix/view.html", {"chart": chart, "grid": grid})


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


def build_matrix_grid(chart):
    """
    Build a 9x9 grid structure for rendering.

    The grid is composed of:
    - Center 3x3: Core goal in center (4,4), 8 pillars around it
    - Outer 8 3x3s: Each pillar's 8 tasks in a 3x3 arrangement

    Returns a list of rows, where each row is a list of cell dicts.
    """
    grid = [[None for _ in range(9)] for _ in range(9)]

    # Center cell (4, 4) - Core Goal
    grid[4][4] = {
        "type": "core_goal",
        "content": chart.core_goal[:50] + "..."
        if len(chart.core_goal) > 50
        else chart.core_goal,
        "completion": chart.completion_percentage,
        "title": "Core Goal",
    }

    # Get all pillars
    pillars = chart.pillar_set.all().order_by("position")

    # Map pillar positions to grid coordinates (8 surrounding the center)
    pillar_coords = {
        1: (3, 3),  # Top-left
        2: (3, 4),  # Top
        3: (3, 5),  # Top-right
        4: (4, 5),  # Right
        5: (5, 5),  # Bottom-right
        6: (5, 4),  # Bottom
        7: (5, 3),  # Bottom-left
        8: (4, 3),  # Left
    }

    # Place pillars
    for pillar in pillars:
        if pillar.position in pillar_coords:
            row, col = pillar_coords[pillar.position]
            grid[row][col] = {
                "type": "pillar",
                "id": pillar.id,
                "content": pillar.name,
                "title": pillar.name,
            }

    # Place tasks in their 3x3 sub-grids
    for pillar in pillars:
        tasks = pillar.task_set.all().order_by("position")

        # Map pillar position to its 3x3 sub-grid
        pillar_pos = pillar.position
        task_grid_map = get_task_grid_map(pillar_pos)

        for task in tasks:
            if task.position in task_grid_map:
                row, col = task_grid_map[task.position]
                grid[row][col] = {
                    "type": "task",
                    "id": task.id,
                    "content": task.title,
                    "status": task.status,
                    "frequency": task.frequency,
                    "title": task.title,
                }

    return grid


def get_task_grid_map(pillar_position):
    """
    Map task positions (1-8) to grid coordinates within a pillar's 3x3 sub-grid.

    Layout for each 3x3 sub-grid:
    1 2 3
    8   4
    7 6 5
    """
    base_row_map = {
        1: (0, 2),  # Top-left  -> (0, 0)
        2: (0, 4),  # Top       -> (0, 1)
        3: (0, 6),  # Top-right -> (0, 2)
        4: (4, 6),  # Right     -> (1, 2)
        5: (8, 6),  # Bottom-right -> (2, 2)
        6: (8, 4),  # Bottom    -> (2, 1)
        7: (8, 2),  # Bottom-left -> (2, 0)
        8: (4, 2),  # Left      -> (1, 0)
    }

    # Map each pillar's sub-grid based on its position
    task_grid_coords = {
        1: {  # Pillar 1 (top-left 3x3)
            1: (2, 0),
            2: (2, 1),
            3: (2, 2),
            4: (3, 2),
            5: (4, 2),
            6: (4, 1),
            7: (4, 0),
            8: (3, 0),
        },
        2: {  # Pillar 2 (top 3x3)
            1: (2, 3),
            2: (2, 4),
            3: (2, 5),
            4: (3, 5),
            5: (4, 5),
            6: (4, 4),
            7: (4, 3),
            8: (3, 3),
        },
        3: {  # Pillar 3 (top-right 3x3)
            1: (2, 6),
            2: (2, 7),
            3: (2, 8),
            4: (3, 8),
            5: (4, 8),
            6: (4, 7),
            7: (4, 6),
            8: (3, 6),
        },
        4: {  # Pillar 4 (right 3x3)
            1: (3, 6),
            2: (3, 7),
            3: (3, 8),
            4: (4, 8),
            5: (5, 8),
            6: (5, 7),
            7: (5, 6),
            8: (4, 6),
        },
        5: {  # Pillar 5 (bottom-right 3x3)
            1: (6, 6),
            2: (6, 7),
            3: (6, 8),
            4: (7, 8),
            5: (8, 8),
            6: (8, 7),
            7: (8, 6),
            8: (7, 6),
        },
        6: {  # Pillar 6 (bottom 3x3)
            1: (6, 3),
            2: (6, 4),
            3: (6, 5),
            4: (7, 5),
            5: (8, 5),
            6: (8, 4),
            7: (8, 3),
            8: (7, 3),
        },
        7: {  # Pillar 7 (bottom-left 3x3)
            1: (6, 0),
            2: (6, 1),
            3: (6, 2),
            4: (7, 2),
            5: (8, 2),
            6: (8, 1),
            7: (8, 0),
            8: (7, 0),
        },
        8: {  # Pillar 8 (left 3x3)
            1: (3, 0),
            2: (3, 1),
            3: (3, 2),
            4: (4, 2),
            5: (5, 2),
            6: (5, 1),
            7: (5, 0),
            8: (4, 0),
        },
    }

    return task_grid_coords.get(pillar_position, {})
