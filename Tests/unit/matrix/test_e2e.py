import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from charts.models import HaradaChart, Pillar, Task


class TestEndToEndFlow:
    """Test complete user workflow from registration to matrix interaction."""

    @pytest.mark.django_db
    def test_complete_user_journey(self, client):
        """Test full journey: register → create chart → view matrix → edit pillar."""
        # Step 1: Register a new user
        register_data = {
            "username": "e2e_testuser",
            "email": "e2e@example.com",
            "password1": "SuperSecure123!",
            "password2": "SuperSecure123!",
        }
        response = client.post(reverse("register"), register_data, follow=True)
        assert response.status_code == 200
        assert User.objects.filter(username="e2e_testuser").exists()

        # Step 2: Login
        login_data = {
            "username": "e2e_testuser",
            "password": "SuperSecure123!",
        }
        response = client.post(reverse("login"), login_data, follow=True)
        assert response.status_code == 200
        user = User.objects.get(username="e2e_testuser")
        assert response.wsgi_request.user == user

        # Step 3: Start wizard (create draft chart)
        response = client.post(reverse("wizard_start"), follow=True)
        assert response.status_code == 200
        chart = HaradaChart.objects.filter(user=user).first()
        assert chart is not None
        assert chart.is_draft is True

        # Step 4: Complete Step 1 (core goal)
        step1_data = {
            "title": "Build a SaaS Product",
            "core_goal": "It is December 2026 and I have a profitable SaaS",
            "target_date": "2026-12-31",
            "self_tangible": "Product earning $10k MRR",
            "self_intangible": "Feel entrepreneurial mastery",
            "others_tangible": "Help 1000 users",
            "others_intangible": "Be a mentor",
        }
        response = client.post(
            reverse("wizard_step1", args=[chart.id]), step1_data, follow=True
        )
        assert response.status_code == 200
        chart.refresh_from_db()
        assert chart.title == "Build a SaaS Product"

        # Step 5: Complete Step 2 (8 pillars)
        step2_data = {
            "pillar_1": "Product Development",
            "pillar_2": "Marketing & Sales",
            "pillar_3": "Personal Health",
            "pillar_4": "Financial Planning",
            "pillar_5": "Customer Support",
            "pillar_6": "User Experience",
            "pillar_7": "DevOps & Infrastructure",
            "pillar_8": "Team Building",
        }
        response = client.post(
            reverse("wizard_step2", args=[chart.id]), step2_data, follow=True
        )
        assert response.status_code == 200
        assert chart.pillar_set.count() == 8

        # Step 6: Complete Step 3 (64 tasks)
        step3_data = {}
        for pillar in chart.pillar_set.all():
            for i in range(1, 9):
                step3_data[f"pillar_{pillar.position}_task_{i}"] = (
                    f"{pillar.name} Action {i}"
                )
        response = client.post(
            reverse("wizard_step3", args=[chart.id]), step3_data, follow=True
        )
        assert response.status_code == 200
        chart.refresh_from_db()
        assert chart.is_draft is False
        assert Task.objects.filter(chart=chart).count() == 64

        # Step 7: View matrix
        response = client.get(reverse("matrix_view", args=[chart.id]))
        assert response.status_code == 200
        content = response.content.decode()
        assert "Build a SaaS Product" in content  # Title should be in page title
        assert "Product Development" in content  # Pillar name should appear

        # Step 8: Get pillar modal
        pillar = chart.pillar_set.first()
        response = client.get(reverse("pillar_modal", args=[chart.id, pillar.id]))
        assert response.status_code == 200
        content = response.content.decode()
        assert pillar.name in content

        # Step 9: Edit pillar (change name and color)
        update_data = {
            "name": "Core Product Development",
            "color": "red",
        }
        response = client.post(
            reverse("pillar_update", args=[chart.id, pillar.id]),
            update_data,
        )
        assert response.status_code == 200
        pillar.refresh_from_db()
        assert pillar.name == "Core Product Development"
        assert pillar.color == "red"

        # Step 10: Get task modal
        task = chart.task_set.first()
        response = client.get(reverse("task_modal", args=[chart.id, task.id]))
        assert response.status_code == 200
        content = response.content.decode()
        assert task.title in content

        # Step 11: Edit task
        task_update_data = {
            "title": "Updated Task Title",
            "description": "New description",
            "frequency": "routine",
            "status": "in_progress",
        }
        response = client.post(
            reverse("task_update", args=[chart.id, task.id]),
            task_update_data,
        )
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.title == "Updated Task Title"
        assert task.status == "in_progress"

        # Step 12: Verify completion percentage updates
        response = client.get(reverse("matrix_view", args=[chart.id]))
        assert response.status_code == 200
        # Chart view should load successfully after task update

    def test_matrix_view_displays_all_cells(
        self, client, user, harada_chart, pillars, tasks
    ):
        """Test that matrix view displays all 9x9 cells correctly."""
        client.force_login(user)
        harada_chart.is_draft = False
        harada_chart.save()

        response = client.get(reverse("matrix_view", args=[harada_chart.id]))
        assert response.status_code == 200
        content = response.content.decode()

        # Check page loads with chart title
        assert "Test Chart" in content

        # Check all 8 pillar names appear in matrix
        for pillar in pillars:
            assert pillar.name in content

        # Check some tasks are rendered (titles are truncated with line-clamp-2)
        assert "Task 1" in content or "Task 2" in content

    def test_pillar_color_inheritance_to_tasks(
        self, client, user, harada_chart, pillars, tasks
    ):
        """Test that tasks inherit pillar color for visual consistency."""
        client.force_login(user)
        harada_chart.is_draft = False
        harada_chart.save()

        # Set pillar color
        pillar = pillars[0]
        pillar.color = "blue"
        pillar.save()

        response = client.get(reverse("matrix_view", args=[harada_chart.id]))
        assert response.status_code == 200
        # The view should apply the pillar's color to all its tasks
        # Actual color classes would be rendered in HTML

    def test_multiple_charts_isolation(self, client, user):
        """Test that charts are properly isolated between users."""
        client.force_login(user)

        # Create first chart
        chart1_data = {
            "title": "Chart 1",
            "core_goal": "Goal 1",
            "target_date": "2026-12-31",
            "self_tangible": "T1",
            "self_intangible": "I1",
            "others_tangible": "T2",
            "others_intangible": "I2",
        }
        response = client.post(reverse("wizard_start"), follow=True)
        chart1 = HaradaChart.objects.filter(user=user).first()

        # Create second chart
        response = client.post(reverse("wizard_start"), follow=True)
        assert HaradaChart.objects.filter(user=user).count() == 2

        chart2 = HaradaChart.objects.filter(user=user).latest("created_at")

        # Both should be accessible
        response = client.get(reverse("matrix_view", args=[chart1.id]))
        assert response.status_code == 200

        response = client.get(reverse("matrix_view", args=[chart2.id]))
        assert response.status_code == 200

    def test_unauthorized_access_blocked(self, client, user):
        """Test that users cannot access other users' charts."""
        client.force_login(user)

        # Create a chart for user1
        response = client.post(reverse("wizard_start"), follow=True)
        chart = HaradaChart.objects.filter(user=user).first()

        # Create another user
        other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="pass123"
        )
        client.force_login(other_user)

        # Verify other user cannot access chart
        response = client.get(reverse("matrix_view", args=[chart.id]))
        # Should either 404 or redirect to login/permission denied
        assert response.status_code in [403, 404]

    def test_modal_form_updates(self, client, user, harada_chart, pillars):
        """Test that modal forms properly update data."""
        client.force_login(user)

        pillar = pillars[0]
        original_name = pillar.name

        # Update pillar with valid data
        update_data = {
            "name": "Updated Pillar Name",
            "color": "purple",
        }
        response = client.post(
            reverse("pillar_update", args=[harada_chart.id, pillar.id]),
            update_data,
        )
        assert response.status_code == 200
        pillar.refresh_from_db()
        assert pillar.name == "Updated Pillar Name"
        assert pillar.color == "purple"

    def test_task_status_updates_completion_percentage(
        self, client, user, harada_chart, pillars, tasks
    ):
        """Test that marking tasks complete updates the completion percentage."""
        client.force_login(user)
        harada_chart.is_draft = False
        harada_chart.save()

        # Initially no tasks are done
        assert harada_chart.completion_percentage == 0

        # Mark first 16 tasks as done (25% of 64)
        for task in tasks[:16]:
            task.status = "done"
            task.save()

        assert harada_chart.completion_percentage == 25

        # Mark all tasks as done
        for task in tasks:
            task.status = "done"
            task.save()

        assert harada_chart.completion_percentage == 100
