from django.urls import path
from . import views

urlpatterns = [
    path("<int:chart_id>/", views.matrix_view, name="matrix_view"),
    path(
        "<int:chart_id>/task/<int:task_id>/modal/", views.task_modal, name="task_modal"
    ),
    path(
        "<int:chart_id>/task/<int:task_id>/update/",
        views.task_update,
        name="task_update",
    ),
]
