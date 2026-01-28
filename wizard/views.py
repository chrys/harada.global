from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from charts.models import HaradaChart, Pillar, Task


@login_required
def wizard_start(request):
    """Start a new Harada chart wizard."""
    if request.method == "POST":
        # Create a new draft chart
        chart = HaradaChart.objects.create(
            user=request.user,
            title="New Chart",
            core_goal="",
            target_date="2026-12-31",
            is_draft=True,
        )
        return redirect("wizard_step1", chart_id=chart.id)

    return render(request, "wizard/start.html")


@login_required
def wizard_step1(request, chart_id):
    """Step 1: Core Goal and Four Perspectives."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)

    if request.method == "POST":
        chart.title = request.POST.get("title", chart.title)
        chart.core_goal = request.POST.get("core_goal", chart.core_goal)
        chart.target_date = request.POST.get("target_date", chart.target_date)
        chart.perspectives = {
            "self_tangible": request.POST.get("self_tangible", ""),
            "self_intangible": request.POST.get("self_intangible", ""),
            "others_tangible": request.POST.get("others_tangible", ""),
            "others_intangible": request.POST.get("others_intangible", ""),
        }
        chart.save()
        return redirect("wizard_step2", chart_id=chart.id)

    return render(request, "wizard/step1.html", {"chart": chart})


@login_required
def wizard_step2(request, chart_id):
    """Step 2: Define 8 Pillars."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)

    if request.method == "POST":
        # Clear existing pillars
        chart.pillar_set.all().delete()

        # Create new pillars
        for i in range(1, 9):
            pillar_name = request.POST.get(f"pillar_{i}", "")
            if pillar_name:
                Pillar.objects.create(chart=chart, name=pillar_name, position=i)

        return redirect("wizard_step3", chart_id=chart.id)

    pillars = chart.pillar_set.all()
    return render(request, "wizard/step2.html", {"chart": chart, "pillars": pillars})


@login_required
def wizard_step3(request, chart_id):
    """Step 3: Define 64 Tasks (8 per pillar)."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)
    pillars = chart.pillar_set.all().order_by("position")

    if not pillars.exists():
        return redirect("wizard_step2", chart_id=chart.id)

    if request.method == "POST":
        # Process tasks for each pillar
        for pillar in pillars:
            for i in range(1, 9):
                task_key = f"pillar_{pillar.position}_task_{i}"
                task_title = request.POST.get(task_key, "")

                if task_title:
                    Task.objects.update_or_create(
                        pillar=pillar,
                        position=i,
                        defaults={
                            "chart": chart,
                            "title": task_title,
                            "description": "",
                            "status": "todo",
                            "frequency": "one_time",
                        },
                    )

        # Finalize the chart
        chart.is_draft = False
        chart.save()
        return redirect("matrix_view", chart_id=chart.id)

    # Get current focused pillar (for HTMX navigation)
    focused_pillar_id = request.GET.get("pillar_id")
    if focused_pillar_id:
        try:
            focused_pillar = pillars.get(id=focused_pillar_id)
        except Pillar.DoesNotExist:
            focused_pillar = pillars.first()
    else:
        focused_pillar = pillars.first()

    tasks = Task.objects.filter(pillar=focused_pillar).order_by("position")

    return render(
        request,
        "wizard/step3.html",
        {
            "chart": chart,
            "pillars": pillars,
            "focused_pillar": focused_pillar,
            "tasks": tasks,
        },
    )


@login_required
def wizard_step3_pillar_view(request, chart_id, pillar_id):
    """HTMX endpoint for changing focused pillar in Step 3."""
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)
    pillar = get_object_or_404(Pillar, id=pillar_id, chart=chart)
    tasks = Task.objects.filter(pillar=pillar).order_by("position")

    return render(
        request, "wizard/step3_pillar.html", {"pillar": pillar, "tasks": tasks}
    )
