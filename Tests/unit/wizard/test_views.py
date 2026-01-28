import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from charts.models import HaradaChart, Pillar, Task


class TestWizardFlow:
    """Test the 3-step wizard flow."""

    def test_wizard_start_view(self, client):
        """Test wizard start page loads."""
        response = client.get(reverse("wizard_start"))
        assert response.status_code == 302  # Redirect to login if not authenticated

    def test_wizard_start_authenticated(self, client, user):
        """Test wizard start for authenticated user."""
        client.force_login(user)
        response = client.get(reverse("wizard_start"))
        assert response.status_code == 200
        assert "Create Your Harada Chart" in response.content.decode()

    def test_wizard_create_chart(self, client, user):
        """Test creating a new chart via wizard start."""
        client.force_login(user)
        response = client.post(reverse("wizard_start"), follow=True)

        # Should redirect to step1
        assert response.status_code == 200
        assert HaradaChart.objects.filter(user=user).exists()

        chart = HaradaChart.objects.filter(user=user).first()
        assert chart.is_draft is True

    def test_wizard_step1_save(self, client, user, harada_chart):
        """Test saving step 1 (core goal)."""
        client.force_login(user)

        data = {
            "title": "My Amazing Goal",
            "core_goal": "It is 2026 and I have achieved my dreams",
            "target_date": "2026-12-31",
            "self_tangible": "Own a business",
            "self_intangible": "Be proud of myself",
            "others_tangible": "Help 100 people",
            "others_intangible": "Be a role model",
        }

        response = client.post(
            reverse("wizard_step1", args=[harada_chart.id]), data, follow=True
        )

        assert response.status_code == 200
        harada_chart.refresh_from_db()
        assert harada_chart.title == "My Amazing Goal"
        assert harada_chart.core_goal == "It is 2026 and I have achieved my dreams"

    def test_wizard_step2_save(self, client, user, harada_chart):
        """Test saving step 2 (8 pillars)."""
        client.force_login(user)

        data = {
            "pillar_1": "Technical Skills",
            "pillar_2": "Marketing",
            "pillar_3": "Health",
            "pillar_4": "Finance",
            "pillar_5": "Community",
            "pillar_6": "Design",
            "pillar_7": "Operations",
            "pillar_8": "Learning",
        }

        response = client.post(
            reverse("wizard_step2", args=[harada_chart.id]), data, follow=True
        )

        assert response.status_code == 200
        assert harada_chart.pillar_set.count() == 8
        assert harada_chart.pillar_set.filter(name="Technical Skills").exists()

    def test_wizard_step3_save(self, client, user, harada_chart, pillars):
        """Test completing step 3 (64 tasks)."""
        client.force_login(user)

        # Create form data with 8 tasks per pillar
        data = {}
        for pillar in pillars:
            for i in range(1, 9):
                data[f"pillar_{pillar.position}_task_{i}"] = f"{pillar.name} Task {i}"

        response = client.post(
            reverse("wizard_step3", args=[harada_chart.id]), data, follow=True
        )

        assert response.status_code == 200
        harada_chart.refresh_from_db()
        assert harada_chart.is_draft is False  # Chart should be finalized
        assert Task.objects.filter(chart=harada_chart).count() == 64
