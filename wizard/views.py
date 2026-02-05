from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from datetime import datetime
from charts.models import HaradaChart, Pillar, Task


def _get_or_create_session_chart(request):
    """Get or create a temporary chart for unauthenticated users."""
    if 'temp_chart_id' not in request.session:
        request.session['temp_chart_id'] = None
        request.session['temp_chart_data'] = {}
    return request.session.get('temp_chart_data', {})


def _save_session_chart_data(request, chart_id, data):
    """Save chart data in session for unauthenticated users."""
    request.session['temp_chart_id'] = chart_id
    request.session['temp_chart_data'] = data
    request.session.modified = True


def _migrate_session_to_database(request, chart_id):
    """Migrate a session-based temporary chart to a real database chart."""
    if not request.user.is_authenticated:
        return None
    
    temp_data = request.session.get('temp_chart_data', {})
    if not temp_data:
        return None
    
    # Create the chart
    target_date_str = temp_data.get('target_date', '2026-12-31')
    if isinstance(target_date_str, str):
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    else:
        target_date = target_date_str
    
    chart = HaradaChart.objects.create(
        user=request.user,
        title=temp_data.get('title', 'Untitled Goal'),
        core_goal=temp_data.get('core_goal', ''),
        target_date=target_date,
        perspectives=temp_data.get('perspectives', {}),
        is_draft=False  # Mark as complete since they finished the wizard
    )
    
    # Create pillars and tasks
    pillars_data = temp_data.get('pillars', {})
    for pillar_num, pillar_data in pillars_data.items():
        if pillar_data.get('name'):
            pillar = Pillar.objects.create(
                chart=chart,
                name=pillar_data['name'],
                position=int(pillar_num)
            )
            
            # Create tasks for this pillar
            tasks_data = pillar_data.get('tasks', {})
            for task_num, task_data in tasks_data.items():
                if task_data.get('title'):
                    Task.objects.create(
                        chart=chart,
                        pillar=pillar,
                        title=task_data['title'],
                        position=int(task_num),
                        status='todo',
                        frequency='one_time'
                    )
    
    # Clear session data
    request.session['temp_chart_id'] = None
    request.session['temp_chart_data'] = {}
    request.session.modified = True
    
    return chart


@csrf_exempt
@require_POST
def create_chart(request):
    """API endpoint to create a new chart with a goal (both authenticated and unauthenticated)."""
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        
        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)
        
        if request.user.is_authenticated:
            # Create a real database chart for authenticated users
            chart = HaradaChart.objects.create(
                user=request.user,
                title=title,
                core_goal=title,
                target_date=datetime.strptime("2026-12-31", "%Y-%m-%d").date(),
                is_draft=True,
            )
            return JsonResponse({
                'chart_id': chart.id,
                'success': True
            })
        else:
            # For unauthenticated users, use a temporary session-based chart
            temp_id = f"temp_{uuid.uuid4().hex[:12]}"
            
            temp_chart_data = {
                'id': temp_id,
                'title': title,
                'core_goal': title,
                'target_date': '2026-12-31',
                'is_draft': True,
                'is_temporary': True,
                'pillars': {},
                'tasks': {}
            }
            
            _save_session_chart_data(request, temp_id, temp_chart_data)
            
            return JsonResponse({
                'chart_id': temp_id,
                'success': True
            })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def wizard_start(request):
    """Start a new Harada chart wizard."""
    if request.method == "POST":
        # Create a new draft chart
        chart = HaradaChart.objects.create(
            user=request.user,
            title="New Chart",
            core_goal="",
            target_date=datetime.strptime("2026-12-31", "%Y-%m-%d").date(),
            is_draft=True,
        )
        return redirect("wizard_step1", chart_id=chart.id)

    return render(request, "wizard/start.html")


def _get_chart(request, chart_id):
    """Get chart from database if authenticated or from session if temporary.
    
    If an authenticated user accesses a temporary chart ID, migrate it to a real chart.
    """
    if str(chart_id).startswith('temp_'):
        # Check if this is an authenticated user accessing a temporary chart
        if request.user.is_authenticated:
            # Migrate the temporary chart to a real database chart
            temp_data = request.session.get('temp_chart_data', {})
            
            # Create a chart from the session data or with a default title
            target_date_str = temp_data.get('target_date', '2026-12-31')
            if isinstance(target_date_str, str):
                target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
            else:
                target_date = target_date_str
            
            chart = HaradaChart.objects.create(
                user=request.user,
                title=temp_data.get('title', 'Untitled Goal'),
                core_goal=temp_data.get('core_goal', ''),
                target_date=target_date,
                perspectives=temp_data.get('perspectives', {}),
                is_draft=True
            )
            # Clear the temporary chart data from session
            request.session['temp_chart_id'] = None
            request.session['temp_chart_data'] = {}
            request.session.modified = True
            # Return the new chart
            return chart
        else:
            # Unauthenticated user, get from session
            return request.session.get('temp_chart_data', {})
    else:
        # Real database chart
        try:
            return HaradaChart.objects.get(id=chart_id)
        except HaradaChart.DoesNotExist:
            return None


def wizard_step1(request, chart_id):
    """Step 1: Core Goal and Four Perspectives."""
    chart = _get_chart(request, chart_id)
    
    if not chart:
        return redirect('home')
    
    # If chart is a database object (migrated from temporary), redirect to the new URL
    if hasattr(chart, 'id') and isinstance(chart.id, int) and str(chart_id).startswith('temp_'):
        return redirect('wizard_step1', chart_id=chart.id)
    
    if request.method == "POST":
        if str(chart_id).startswith('temp_'):
            # Update session-based temporary chart
            chart['title'] = request.POST.get("title", chart.get('title', ''))
            chart['core_goal'] = request.POST.get("core_goal", chart.get('core_goal', ''))
            chart['target_date'] = request.POST.get("target_date", chart.get('target_date', '2026-12-31'))
            chart['perspectives'] = {
                "self_tangible": request.POST.get("self_tangible", ""),
                "self_intangible": request.POST.get("self_intangible", ""),
                "others_tangible": request.POST.get("others_tangible", ""),
                "others_intangible": request.POST.get("others_intangible", ""),
            }
            _save_session_chart_data(request, chart_id, chart)
        else:
            # Update database chart (requires authentication)
            if not request.user.is_authenticated:
                return redirect('sign_up')
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
        
        return redirect("wizard_step2", chart_id=chart_id)

    return render(request, "wizard/step1.html", {"chart": chart})



def wizard_step2(request, chart_id):
    """Step 2: Define 8 Pillars."""
    chart = _get_chart(request, chart_id)
    
    if not chart:
        return redirect('home')
    
    # If chart is a database object (migrated from temporary), redirect to the new URL
    if hasattr(chart, 'id') and isinstance(chart.id, int) and str(chart_id).startswith('temp_'):
        return redirect('wizard_step2', chart_id=chart.id)

    if request.method == "POST":
        if str(chart_id).startswith('temp_'):
            # Update session-based temporary chart pillars
            if 'pillars' not in chart:
                chart['pillars'] = {}
            
            # Clear existing pillars and save new ones
            chart['pillars'] = {}
            for i in range(1, 9):
                pillar_name = request.POST.get(f"pillar_{i}", "")
                if pillar_name:
                    chart['pillars'][str(i)] = {
                        'name': pillar_name, 
                        'position': i,
                        'tasks': {}
                    }
            _save_session_chart_data(request, chart_id, chart)
        else:
            # Update database chart pillars (requires authentication)
            if not request.user.is_authenticated:
                return redirect('sign_up')
            
            # Clear existing pillars
            chart.pillar_set.all().delete()

            # Create new pillars
            for i in range(1, 9):
                pillar_name = request.POST.get(f"pillar_{i}", "")
                if pillar_name:
                    Pillar.objects.create(chart=chart, name=pillar_name, position=i)

        return redirect("wizard_step3", chart_id=chart_id)

    # Get pillars for display
    if str(chart_id).startswith('temp_'):
        pillars = chart.get('pillars', {})
        # Convert to list format for template
        pillar_list = []
        for i in range(1, 9):
            pillar_data = pillars.get(str(i), {})
            pillar_list.append({
                'position': i,
                'name': pillar_data.get('name', '')
            })
        pillars = pillar_list
    else:
        pillars = chart.pillar_set.all()
    
    return render(request, "wizard/step2.html", {"chart": chart, "pillars": pillars})


def wizard_step3(request, chart_id):
    """Step 3: Define 64 Tasks (8 per pillar)."""
    chart = _get_chart(request, chart_id)
    
    if not chart:
        return redirect('home')
    
    # If chart is a database object (migrated from temporary), redirect to the new URL
    if hasattr(chart, 'id') and isinstance(chart.id, int) and str(chart_id).startswith('temp_'):
        return redirect('wizard_step3', chart_id=chart.id)

    # Get pillars based on chart type
    if str(chart_id).startswith('temp_'):
        pillars_data = chart.get('pillars', {})
        if not pillars_data:
            return redirect("wizard_step2", chart_id=chart_id)
        
        # Convert to list for template
        pillars = []
        for i in range(1, 9):
            pillar_data = pillars_data.get(str(i), {})
            if pillar_data.get('name'):
                tasks = []
                tasks_data = pillar_data.get('tasks', {})
                for j in range(1, 9):
                    task = tasks_data.get(str(j), {})
                    tasks.append({
                        'position': j,
                        'title': task.get('title', '')
                    })
                
                pillars.append({
                    'position': i,
                    'name': pillar_data.get('name', ''),
                    'tasks': tasks
                })
    else:
        # Database chart - requires authentication
        if not request.user.is_authenticated:
            return redirect('sign_up')
        pillars = chart.pillar_set.all().order_by("position")
        if not pillars.exists():
            return redirect("wizard_step2", chart_id=chart_id)

    if request.method == "POST":
        if str(chart_id).startswith('temp_'):
            # Handle temporary chart task updates
            pillars_data = chart.get('pillars', {})
            
            for i in range(1, 9):
                if str(i) in pillars_data:
                    if 'tasks' not in pillars_data[str(i)]:
                        pillars_data[str(i)]['tasks'] = {}
                    
                    for j in range(1, 9):
                        task_key = f"pillar_{i}_task_{j}"
                        task_title = request.POST.get(task_key, "")
                        if task_title:
                            pillars_data[str(i)]['tasks'][str(j)] = {
                                'title': task_title,
                                'position': j
                            }
            
            chart['pillars'] = pillars_data
            _save_session_chart_data(request, chart_id, chart)
            
            # Check if this is a "Complete Chart" action
            if 'complete_chart' in request.POST:
                # Require authentication to complete
                if not request.user.is_authenticated:
                    return redirect(f'/sign-up?redirect=/wizard/{chart_id}/step3/')
                
                # User is authenticated, migrate to real chart
                migrated_chart = _migrate_session_to_database(request, chart_id)
                if migrated_chart:
                    return redirect("matrix_view", chart_id=migrated_chart.id)
                else:
                    return redirect('home')
            else:
                # Just save and stay on same page
                return redirect("wizard_step3", chart_id=chart_id)
        else:
            # Database chart - process normally
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

    return render(
        request,
        "wizard/step3.html",
        {
            "chart": chart,
            "chart_id": chart_id,
            "pillars": pillars,
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
