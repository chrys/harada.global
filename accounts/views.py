from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError


def register(request):
    """User registration view."""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            return render(
                request, "accounts/register.html", {"error": "Passwords do not match"}
            )

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            login(request, user)
            return redirect("dashboard")
        except IntegrityError:
            return render(
                request,
                "accounts/register.html",
                {"error": "Username or email already exists"},
            )

    return render(request, "accounts/register.html")


def login_view(request):
    """User login view."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(
                request, "accounts/login.html", {"error": "Invalid credentials"}
            )

    return render(request, "accounts/login.html")


@login_required
@require_http_methods(["POST"])
def logout_view(request):
    """User logout view."""
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    """User dashboard showing all charts."""
    charts = request.user.harada_charts.all()
    return render(request, "accounts/dashboard.html", {"charts": charts})
