import pytest
from django.contrib.auth.models import User
from charts.models import HaradaChart, Pillar, Task


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def harada_chart(db, user):
    """Create a test Harada chart."""
    return HaradaChart.objects.create(
        user=user,
        title="Test Chart",
        core_goal="Launch a website by end of 2026",
        target_date="2026-12-31",
        is_draft=True,
        perspectives={
            "self_tangible": "Owning a live URL",
            "self_intangible": "Mastering full-stack",
            "others_tangible": "Solving problems for users",
            "others_intangible": "Being a role model",
        },
    )


@pytest.fixture
def pillars(db, harada_chart):
    """Create 8 pillars for a test chart."""
    pillar_names = [
        "Technical Skills",
        "Marketing",
        "Mental Health",
        "Finance",
        "Community",
        "Design",
        "Operations",
        "Learning",
    ]
    pillars = []
    for i, name in enumerate(pillar_names, 1):
        pillar = Pillar.objects.create(chart=harada_chart, name=name, position=i)
        pillars.append(pillar)
    return pillars


@pytest.fixture
def tasks(db, pillars):
    """Create 64 tasks (8 per pillar)."""
    tasks_list = []
    for pillar in pillars:
        for i in range(1, 9):
            task = Task.objects.create(
                chart=pillar.chart,
                pillar=pillar,
                title=f"{pillar.name} Task {i}",
                description=f"Description for {pillar.name} Task {i}",
                frequency="one_time" if i % 2 == 0 else "routine",
                status="todo",
                position=i,
            )
            tasks_list.append(task)
    return tasks_list
