import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestMobileModals:
    """Test mobile-specific modal (bottom sheet) behavior."""

    def test_task_modal_has_bottom_sheet_classes(self, client, user, harada_chart, pillars, tasks):
        """Test that task modal includes classes for bottom sheet on mobile."""
        client.force_login(user)
        task = tasks[0]
        url = reverse('task_modal', args=[harada_chart.id, task.id])
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode()

        # Check for bottom-sheet logic (fixed inset-0 with items-end)
        assert "fixed inset-0" in content
        assert "items-end" in content
        assert "sm:items-center" in content
        assert "rounded-t-2xl" in content
        assert "sm:rounded-lg" in content
        assert "pb-safe" in content
