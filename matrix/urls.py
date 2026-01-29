from django.urls import path
from . import views

urlpatterns = [
    path("<int:chart_id>/", views.matrix_view, name="matrix_view"),
    path(
        "<int:chart_id>/pillar/<int:pillar_id>/modal/",
        views.pillar_modal,
        name="pillar_modal",
    ),
    path(
        "<int:chart_id>/pillar/<int:pillar_id>/update/",
        views.pillar_update,
        name="pillar_update",
    ),
    path(
        "<int:chart_id>/task/<int:task_id>/modal/", views.task_modal, name="task_modal"
    ),
    path(
        "<int:chart_id>/task/<int:task_id>/update/",
        views.task_update,
        name="task_update",
    ),

    path(
        "<int:chart_id>/pillar/<int:pillar_id>/task/<int:position>/modal/",
        views.task_create_modal,
        name="task_create_modal",
    ),
    path(
        "<int:chart_id>/pillar/<int:pillar_id>/task/<int:position>/create/",
        views.task_create,
        name="task_create",
    ),
]
