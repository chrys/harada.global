from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("sign-up/", views.sign_up, name="sign_up"),
    path("sign-in/", views.sign_in, name="sign_in"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("chart/<int:chart_id>/delete/", views.delete_chart, name="delete_chart"),
]
