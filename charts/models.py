from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class HaradaChart(models.Model):
    """
    Represents a 64-cell Harada Method chart.
    Composed of 8 pillars with 8 tasks each.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="harada_charts"
    )
    title = models.CharField(max_length=255)
    core_goal = models.TextField(help_text="The long-term goal")
    target_date = models.DateField()
    is_draft = models.BooleanField(
        default=True, help_text="True while completing wizard steps"
    )
    perspectives = models.JSONField(
        default=dict,
        help_text="Four perspectives: self_tangible, self_intangible, others_tangible, others_intangible",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    @property
    def completion_percentage(self):
        """Calculate completion % based on tasks marked 'done'."""
        tasks = self.task_set.all()
        if tasks.count() == 0:
            return 0
        done_count = tasks.filter(status="done").count()
        return round((done_count / tasks.count()) * 100)


class Pillar(models.Model):
    """
    One of 8 high-level themes/areas that compose the Harada Chart.
    """

    COLOR_CHOICES = [
        ("blue", "Blue"),
        ("red", "Red"),
        ("green", "Green"),
        ("purple", "Purple"),
        ("yellow", "Yellow"),
        ("pink", "Pink"),
        ("indigo", "Indigo"),
        ("orange", "Orange"),
    ]

    chart = models.ForeignKey(HaradaChart, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default="blue",
        help_text="Color for this pillar and its tasks",
    )
    position = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text="Position 1-8 around the center cell",
    )

    class Meta:
        unique_together = ("chart", "position")
        ordering = ["position"]

    def __str__(self):
        return f"{self.name} (Pillar {self.position})"


class Task(models.Model):
    """
    One of 64 action items. Each pillar contains 8 tasks.
    """

    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    FREQUENCY_CHOICES = [
        ("one_time", "One-time"),
        ("routine", "Routine"),
    ]

    chart = models.ForeignKey(HaradaChart, on_delete=models.CASCADE)
    pillar = models.ForeignKey(Pillar, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default="one_time"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    position = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text="Position 1-8 within the pillar's 3x3 grid",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("pillar", "position")
        ordering = ["pillar", "position"]

    def __str__(self):
        return f"{self.title} ({self.pillar.name})"
