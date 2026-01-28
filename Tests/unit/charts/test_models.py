import pytest
from django.contrib.auth.models import User
from charts.models import HaradaChart, Pillar, Task


class TestHaradaChartModel:
    """Test HaradaChart model."""

    def test_create_harada_chart(self, harada_chart):
        """Test creating a Harada chart."""
        assert harada_chart.id is not None
        assert harada_chart.title == "Test Chart"
        assert harada_chart.is_draft is True

    def test_completion_percentage_no_tasks(self, harada_chart):
        """Test completion percentage with no tasks."""
        assert harada_chart.completion_percentage == 0

    def test_completion_percentage_with_tasks(self, harada_chart, tasks):
        """Test completion percentage calculation."""
        assert harada_chart.completion_percentage == 0  # All tasks are 'todo'

        # Mark half the tasks as done
        for task in tasks[:32]:
            task.status = "done"
            task.save()

        assert harada_chart.completion_percentage == 50

    def test_completion_percentage_all_done(self, harada_chart, tasks):
        """Test completion percentage when all tasks are done."""
        for task in tasks:
            task.status = "done"
            task.save()

        assert harada_chart.completion_percentage == 100


class TestPillarModel:
    """Test Pillar model."""

    def test_create_pillar(self, pillars):
        """Test creating a pillar."""
        assert len(pillars) == 8
        assert pillars[0].position == 1
        assert pillars[7].position == 8

    def test_pillar_unique_constraint(self, harada_chart, pillars):
        """Test that position is unique per chart."""
        with pytest.raises(Exception):
            Pillar.objects.create(
                chart=harada_chart,
                name="Duplicate",
                position=1,  # This position already exists
            )


class TestTaskModel:
    """Test Task model."""

    def test_create_task(self, tasks):
        """Test creating a task."""
        assert len(tasks) == 64
        assert tasks[0].position == 1
        assert tasks[0].status == "todo"

    def test_task_status_choices(self, tasks):
        """Test task status choices."""
        task = tasks[0]
        task.status = "in_progress"
        task.save()
        assert task.status == "in_progress"

        task.status = "done"
        task.save()
        assert task.status == "done"

    def test_task_frequency_choices(self, tasks):
        """Test task frequency choices."""
        task = tasks[0]
        task.frequency = "routine"
        task.save()
        assert task.frequency == "routine"

    def test_task_unique_constraint(self, pillars):
        """Test that position is unique per pillar."""
        pillar = pillars[0]
        # Create first task
        Task.objects.create(
            chart=pillar.chart, pillar=pillar, title="Task 1", position=1
        )

        # Try to create duplicate position
        with pytest.raises(Exception):
            Task.objects.create(
                chart=pillar.chart, pillar=pillar, title="Task 2", position=1
            )
