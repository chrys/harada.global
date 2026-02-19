from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from charts.models import HaradaChart


def sign_in(request):
    """Sign in view with Clerk."""
    return render(request, "accounts/login.html", {
        "clerk_publishable_key": settings.CLERK_PUBLISHABLE_KEY
    })


def sign_up(request):
    """Sign up view with Clerk."""
    # Get redirect URL from query parameters or session
    redirect_url = request.GET.get('redirect') or request.session.get('redirect_after_signup', '/dashboard')
    
    return render(request, "accounts/register.html", {
        "clerk_publishable_key": settings.CLERK_PUBLISHABLE_KEY,
        "redirect_after_signup": redirect_url
    })


def long_term_goal(request):
    """Long-term Goal method page."""
    return render(request, "method/long_term_goal.html")


def five_pillars(request):
    """Five Pillars method page."""
    return render(request, "method/five_pillars.html")


def tasks_64(request):
    """64 Tasks method page."""
    return render(request, "method/64_tasks.html")


@login_required
def dashboard(request):
    """User dashboard showing all charts."""
    charts = request.user.harada_charts.all()
    return render(request, "accounts/dashboard.html", {"charts": charts})


@login_required
def delete_chart(request, chart_id):
    """
    Delete a chart after user confirmation.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.
    chart_id : int
        The ID of the chart to delete.

    Returns
    -------
    HttpResponse
        Redirects to dashboard on successful deletion.
    """
    chart = get_object_or_404(HaradaChart, id=chart_id, user=request.user)
    chart.delete()
    return redirect("dashboard")




