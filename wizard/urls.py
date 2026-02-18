from django.urls import path
from . import views

urlpatterns = [
    path("create-chart/", views.create_chart, name="create_chart"),
    path("start/", views.wizard_start, name="wizard_start"),
    path("<chart_id>/step1/", views.wizard_step1, name="wizard_step1"),
    path("<chart_id>/ai-inspiration/", views.ai_inspiration, name="ai_inspiration"),
    path("<chart_id>/step2/", views.wizard_step2, name="wizard_step2"),
    path("<chart_id>/step3/", views.wizard_step3, name="wizard_step3"),
    path(
        "<int:chart_id>/step3/pillar/<int:pillar_id>/",
        views.wizard_step3_pillar_view,
        name="wizard_step3_pillar",
    ),
]
