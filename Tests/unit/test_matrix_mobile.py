import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestMatrixMobileView:
    """Test the mobile-optimized matrix view."""

    def test_matrix_view_has_mobile_elements(self, client, user, harada_chart, pillars):
        """Test that the matrix view includes mobile-specific HTML elements."""
        client.force_login(user)
        url = reverse('matrix_view', args=[harada_chart.id])
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode()

        # Check for mobile container
        assert "md:hidden space-y-4" in content
        # Check for Core Goal card in mobile view
        assert "Core Goal" in content
        # Check for accordion details/summary
        assert "<details" in content
        assert "<summary" in content
        # Check for pillar names in mobile view
        for pillar in pillars:
            assert pillar.name in content

    def test_matrix_mobile_view_has_add_task_links(self, client, user):
        """Test that the mobile view contains HTMX links to add tasks when empty."""
        client.force_login(user)
        # Create a chart with one pillar but NO tasks
        from charts.models import HaradaChart, Pillar
        chart = HaradaChart.objects.create(
            user=user, title="Empty Chart", core_goal="Goal", target_date="2026-12-31"
        )
        pillar = Pillar.objects.create(chart=chart, name="Pillar 1", position=1)
        
        url = reverse('matrix_view', args=[chart.id])
        response = client.get(url)
        content = response.content.decode()
        
        # Check for task create modal URL structure in HTMX attribute
        # Example: hx-get="/matrix/1/pillar/1/task/1/modal/"
        assert '/task/1/modal/' in content
        assert 'hx-get=' in content

